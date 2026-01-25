document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.getElementById('carousel-inner');
  const container = document.querySelector('.carousel');

  // Дублируем отзывы для бесконечной прокрутки
  carousel.innerHTML += carousel.innerHTML;

  let position = 0;
  const speed = 0.5; // скорость движения
  let isPaused = false;

  function animate() {
    if (!isPaused) {
      position -= speed;
      if (Math.abs(position) >= carousel.scrollWidth / 2) {
        position = 0; // сброс при достижении конца
      }
      carousel.style.transform = `translateX(${position}px)`;
    }
    requestAnimationFrame(animate);
  }

  // Наведение — ставим на паузу
  container.addEventListener('mouseenter', () => {
    isPaused = true;
  });

  // Убираем курсор — продолжаем
  container.addEventListener('mouseleave', () => {
    isPaused = false;
  });

  animate();
});