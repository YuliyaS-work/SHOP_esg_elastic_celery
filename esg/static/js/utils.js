// получаем куки корзины
function getBasketFromCookies() {
  try {
    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith('basket='));
    if (!cookie) return {};
    const value = decodeURIComponent(cookie.split('=')[1]);
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch (e) {
    console.warn('Ошибка чтения куки basket:', e);
    return {};
  }
}

// Сохраняем куки корзины с добавдением итоговой стоимости
function saveBasketToCookies(basket) {
  // пересчитываем общую стоимость
  let totalSum = 0;
  Object.entries(basket).forEach(([key, value]) => {
    if (key !== 'generalCost') {
      const [quantity, price] = value;
      totalSum += parseFloat(price);
    }
  });
  basket.generalCost = totalSum.toFixed(2);
  // Работает и на http, и на https
  const isSecure = location.protocol === 'https:';
  document.cookie = `basket=${encodeURIComponent(JSON.stringify(basket))}; path=/; max-age=2592000; SameSite=Lax${isSecure ? '; Secure' : ''}`;
}

// Очищаем куки корзины
function clearBasketCookies() {
  document.cookie = 'basket=; path=/; max-age=0';
}

// Получение токена
function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return '';
}


// функции получения, сохранения просмотренных товаров, на каждой странице
window.getViewedProducts = function() {
  const stored = localStorage.getItem('viewedProducts');
  return stored ? JSON.parse(stored) : [];
};

function saveViewedProduct(product) {
  const viewedProduct = {
    id: product.id,
    title: product.title,
    product_title_translit: product.product_title_translit,
    price: product.price,
    photo: product.photo,
    subrubric_title_translit: product.subrubric_title_translit,
    rubric_name_translit: product.rubric_name_translit,
    url: product.url
  };

  let products = getViewedProducts();
  products = products.filter(p => p.id !== viewedProduct.id);
  products.unshift(viewedProduct);
  if (products.length > 10) {
    products = products.slice(0, 10);
  }

  localStorage.setItem('viewedProducts', JSON.stringify(products));
}