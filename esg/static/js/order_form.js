document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('order-form');
  const url = form.dataset.url;
  const overlay = document.getElementById('overlay');
  const responseMessageError = document.getElementById('response-message-error');

// Достаем куки корзины
  const rawBasket = document.cookie
    .split('; ')
    .find(row => row.startsWith('basket='));
  const basket = rawBasket ? JSON.parse(decodeURIComponent(rawBasket.split('=')[1])) : {};
  const generalCost = basket.generalCost || '0.00';

// Заполнение формы
  if (!form.dataset.handlerAttached) {

//    // убирает ошибку при изменении какого-либо поля
//    form.querySelectorAll('input, textarea, select').forEach(field => {
//    field.addEventListener('input', () => {
//      responseMessageError.innerText = '';
//      });
//    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());
      data.basket = basket;
      data.generalCost = generalCost;

        fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(data),
        credentials: 'include'
      })
      .then(res => {
        if (!res.ok) throw new Error('Что-то пошло не так. Проверьте Ваши данные.');
        return res.json();
      })
      .then(data => {
        alert('☑️ Заказ успешно создан!');
        form.reset();
        overlay.classList.remove('active');
        form.classList.remove('active');

        window.basket = {};
        clearBasketCookies();
        document.getElementById('basket').innerHTML = '<p>Корзина пуста</p>';

        refreshAllBasketButtons(window.basket);
      })
      .catch(err => {
        responseMessageError.innerText = err.message;
      });

    });

    form.dataset.handlerAttached = 'true';
  }

// Работа с окошком формы
  overlay.addEventListener('click', () => {
    overlay.classList.remove('active');
    form.classList.remove('active');
  });
});
(function() {
  const alertBox = document.getElementById('order-alert');
  const alertMessage = document.getElementById('order-alert-message');
  const alertBtn = document.getElementById('order-alert-btn');

  window.alert = function(message) {
    alertMessage.textContent = message;
    alertBox.classList.add('active');

    // скрыть автоматически через 3 сек
    setTimeout(() => {
      alertBox.classList.remove('active');
    }, 3000);
  };

});