
const list = document.querySelector('.subcategories-list');
const btnLeft = document.querySelector('.carousel-btn.left');
const btnRight = document.querySelector('.carousel-btn.right');

btnLeft.addEventListener('click', () => {
  list.scrollBy({ left: -200, behavior: 'smooth' });
});

btnRight.addEventListener('click', () => {
  list.scrollBy({ left: 200, behavior: 'smooth' });
});