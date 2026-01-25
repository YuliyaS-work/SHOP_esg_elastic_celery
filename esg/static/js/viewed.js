function renderViewedProducts() {
//  console.log('LocalStorage:', localStorage.getItem('viewedProducts'));
  const products = getViewedProducts();
//  console.log('Просмотренные товары:', products);

  if (products.length === 0) return;

  const container = document.createElement('div');
  container.className = 'viewed-products';
  container.innerHTML = `
    <div style="text-align: center; margin-bottom: 10px; margin-top: 10px;">
      <h2 style="color: black; border-bottom: 2px solid #e6c200; display: inline-block; padding-bottom: 5px;">Вы смотрели</h2>
    </div>
  `;
  // === вот эта новая оболочка ===
const wrapper = document.createElement('div');
wrapper.className = 'carousel-wrapper';
// =================================
  const carousel = document.createElement('div');
  carousel.className = 'viewed-carousel';

 const basket = getBasketFromCookies();

  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-new-catalog';

    const photoUrl = product.photo && product.photo.trim() !== ''
      ? product.photo
      : '/static/image/default-product.png';

     const href = product.url || '/';

  // формируем блок цены обычным if
let priceBlock = '';
const rawPrice = product.price;
const priceNum = parseFloat(String(rawPrice).replace(',', '.'));

if (!isNaN(priceNum) && priceNum > 0) {
  const formattedPrice = priceNum.toFixed(2).replace('.', ',');
  priceBlock = `
    <p class="price">${formattedPrice} BYN</p>
    <button type="button" class="basket"
            data-title="${product.title}"
            data-price="${formattedPrice}">
      Купить
    </button>
  `;
} else {
  priceBlock = `<p class="price_no">Уточняйте цену</p>`;
}

    card.innerHTML = `
      <img src="${photoUrl}" alt="${product.title}">
      <a href="${href}" class="product-title"
         data-id="${product.id}"
         data-title="${product.title}"
         data-product_title_translit = "${product.product_title_translit}"
         data-photo="${product.photo}"
         data-price="${product.price}"
         data-subrubric_title_translit="${product.subrubric_title_translit}"
         data-rubric_name_translit="${product.rubric_name_translit}"
         data-url="${href}">
        <h3>${product.title}</h3>
      </a>
      <div class="card-bottom">
       ${priceBlock}
      </div>
    `;
    carousel.appendChild(card);
  });

  wrapper.appendChild(carousel);
  container.appendChild(wrapper);

  const target = document.querySelector('#viewed-products-container');
  if (target) {
    target.innerHTML = '';
    target.appendChild(container);

    container.querySelectorAll('.basket').forEach(button => {
      const title = button.dataset.title;
      const rawPrice = button.dataset.price;
      const price = parseFloat(rawPrice.replace(',', '.')).toFixed(2);

      // Установим начальное состояние кнопки
      const currentBasket = getBasketFromCookies();
      if (currentBasket[title]) {
        button.textContent = 'В корзине';
        button.classList.add('in-basket');
      } else {
        button.textContent = 'Купить';
        button.classList.remove('in-basket');
      }

      button.addEventListener('click', () => {
        const updatedBasket = getBasketFromCookies();

        if (updatedBasket[title]) {
          delete updatedBasket[title];
          button.textContent = 'Купить';
          button.classList.remove('in-basket');
        } else {
          updatedBasket[title] = [1, price];
          button.textContent = 'В корзине';
        button.classList.add('in-basket');
        }

        saveBasketToCookies(updatedBasket);
        window.basket = updatedBasket;

        if (typeof renderBasket === 'function') {
          renderBasket();
          refreshAllBasketButtons(window.basket);
        }
      });
    });

    container.querySelectorAll('.product-title').forEach(link => {
      link.addEventListener('click', () => {
        const product = {
          id: link.dataset.id,
          photo: link.dataset.photo,
          title: link.dataset.title,
          product_title_translit: link.dataset.product_title_translit,
          price: link.dataset.price,
          subrubric_title_translit: link.dataset.subrubric_title_translit,
          rubric_name_translit: link.dataset.rubric_name_translit,
          url: link.dataset.url
        };
        saveViewedProduct(product);
      });
    });
  } else {
//    console.warn('viewed-products-container не найден');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderViewedProducts();

  document.querySelectorAll('.product-title').forEach(link => {
    link.addEventListener('click', () => {

      const product = {
        id: link.dataset.id,
        photo: link.dataset.photo,
        title: link.dataset.title,
        product_title_translit: link.dataset.product_title_translit,
        price: link.dataset.price,
        subrubric_title_translit: link.dataset.subrubric_title_translit,
        rubric_name_translit: link.dataset.rubric_name_translit,
        url: link.dataset.url
      };
//      console.log('Сохраняем из каталога:', product);
      saveViewedProduct(product);
    });
  });
});

