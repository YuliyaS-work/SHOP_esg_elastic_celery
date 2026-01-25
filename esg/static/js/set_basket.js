document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.basket');
  let basket = getBasketFromCookies();

  buttons.forEach(button => {
    const productTitle = button.dataset.title;
    const productPrice = parseFloat(button.dataset.price.replace(',', '.')).toFixed(2);


    // Устанавливаем начальное состояние кнопки
    if (basket[productTitle]) {
      button.textContent = 'В корзине';
      button.classList.add('in-basket');
    } else {
      button.textContent = 'Купить';
      button.classList.remove('in-basket');
    }

    button.addEventListener('click', () => {
      if (basket[productTitle]) {
        // Удаление из корзины
        delete basket[productTitle];
        saveBasketToCookies(basket);
        button.textContent = 'Купить';
        button.classList.remove('in-basket');
      } else {
        // Добавление в корзину
        basket[productTitle] = [1, productPrice];
        saveBasketToCookies(basket);
        button.textContent = 'В корзине';
        button.classList.add('in-basket');
      }
    });
  });
 });