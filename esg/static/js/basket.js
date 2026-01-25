// обновление корзины
function updateBasketButton(button, basket) {
  const productTitle = button.dataset.title;
  if (basket[productTitle]) {
    button.textContent = 'В корзине';
    button.classList.add('in-basket');
  } else {
    button.textContent = 'Купить';
    button.classList.remove('in-basket');
  }
}

// перезагрузка кнопок купить и удалить при рабзоте с корзиной
function refreshAllBasketButtons(basket) {
  document.querySelectorAll('.basket').forEach(btn => {
    updateBasketButton(btn, basket);
  });
}

// функция рендера окошка корзины из куков
function renderBasket() {
  const basketContainer = document.getElementById('basket');
  if (!basketContainer) return;

  basketContainer.innerHTML = '';
  const titles = Object.keys(window.basket).filter(key => key !== 'generalCost');

  if (titles.length === 0) {
    basketContainer.innerHTML = `
    <div class="empty-basket">
      <img src="/static/image/basket.png" alt="Корзина пуста" class="empty-basket-img flip">
      <p>Корзина пуста</p>
    </div>
  `;
    return;
  }

  let totalCost = 0;

  // рендер каждого товара в окошке корзины
  titles.forEach(title => {
    const [quantity, price] = window.basket[title];
    const unitPrice = parseFloat(price) / quantity;
    const totalPrice = (quantity * unitPrice).toFixed(2);
    totalCost += parseFloat(totalPrice);

// форматируем только для отображения
    const displayTotalPrice = totalPrice.replace('.', ',');

    const div = document.createElement('div');
    div.className = 'basket-item';
    div.innerHTML = `
      <span class="title">${title}</span>
      <span class="price_b">${displayTotalPrice} BYN</span>
       <div class="controls">
      <button class="decrease">−</button>
      <span class="quantity">${quantity}</span>
      <button class="increase">+</button>
      <button class="remove">🗑️</button>
      </div>
    `;
//  увеличение количества и цены каждого товара
    div.querySelector('.increase').onclick = () => {
      window.basket[title][0]++;
      const newQuantity = window.basket[title][0];
      const newTotalPrice = (newQuantity * unitPrice).toFixed(2);
      window.basket[title][1] = newTotalPrice;
      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    };

//  уменьшение количества и цены каждого товара
    div.querySelector('.decrease').onclick = () => {
      window.basket[title][0]--;
      const newQuantity = window.basket[title][0];
      if (newQuantity <= 0) {
        delete window.basket[title];
      } else {
        const newTotalPrice = (newQuantity * unitPrice).toFixed(2);
        window.basket[title][1] = newTotalPrice;
      }
      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    };
//  удаление товара из корзины при нажатии на иконку корзины
    div.querySelector('.remove').onclick = () => {
      delete window.basket[title];
      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    };

    basketContainer.appendChild(div);
  });

//  рендер общей стоимости
  window.basket.generalCost = totalCost.toFixed(2);

  const displayGeneralCost = window.basket.generalCost.replace('.', ','); // форматируем для вывода

  const totalDiv = document.createElement('div');
  totalDiv.className = 'basket-total';
  totalDiv.innerHTML = `<strong class="currency">Итого: ${displayGeneralCost} BYN</strong>`;
  basketContainer.appendChild(totalDiv);

// открытие формы формления заказа
  if (!document.querySelector('.open-order-form')) {
    const orderButton = document.createElement('button');
    orderButton.textContent = 'Оформить заказ';
    orderButton.classList.add('order-btn', 'open-order-form');
    basketContainer.appendChild(orderButton);
  }
}

document.addEventListener('DOMContentLoaded', () => {
window.basket = getBasketFromCookies();
renderBasket();

  const form = document.getElementById('order-form');
  const overlay = document.getElementById('overlay');


// добавление из каруселек
  document.querySelectorAll('.basket').forEach(button => {
    const productTitle = button.dataset.title;
    const productPrice = parseFloat(button.dataset.price.replace(',', '.')).toFixed(2);

    updateBasketButton(button, window.basket);

    button.addEventListener('click', () => {
      if (window.basket[productTitle]) {
        delete window.basket[productTitle];
      } else {
        window.basket[productTitle] = [1, productPrice];
      }

      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    });
  });

  renderBasket();

// кликабельность окошка
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('open-order-form')) {
      overlay.classList.add('active');
      form.classList.add('active');
    }
  });

  const closeBtn = document.getElementById('close-order-form');
  const closeModal = () => {
    overlay.classList.remove('active');
    form.classList.remove('active');
  };
  overlay.addEventListener('click', closeModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
});

