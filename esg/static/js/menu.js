document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.menu-toggle'); // все кнопки-бургеры
  const overlays = document.querySelectorAll('.overlay_menu'); // все overlay

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      document.body.classList.toggle('sidebar-open');
    });
  });

  overlays.forEach(overlay => {
    overlay.addEventListener('click', () => {
      document.body.classList.remove('sidebar-open');
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') document.body.classList.remove('sidebar-open');
  });
});