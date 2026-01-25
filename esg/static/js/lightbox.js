document.addEventListener("DOMContentLoaded", () => {
  const certPhoto = document.getElementById('certificate-photo');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');

  certPhoto.addEventListener('click', () => {
    lightboxImg.src = certPhoto.src;
    lightbox.style.display = 'flex';
  });

  lightbox.addEventListener('click', () => {
    lightbox.style.display = 'none';
  });
});