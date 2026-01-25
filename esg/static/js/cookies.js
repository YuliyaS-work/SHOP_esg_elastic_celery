document.addEventListener('DOMContentLoaded', () => {
  const SHOW_INTERVAL = 24 * 60 * 60 * 1000; // 24 часа

// Сохранение согласия или отказа от куков
  function saveCookieConsent(consent) {
    const maxAge = 2592000; // 30 дней
    const value = consent ? 'true' : 'false';
    const isLocalhost = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    const secureFlag = isLocalhost ? '' : '; Secure';
    const isSecure = location.protocol === 'https:';
    document.cookie = `cookieConsent=${value}; path=/; max-age=${maxAge}; SameSite=Lax${secureFlag}`;
  }

// Баннер с куками
  function shouldShowCookieBanner() {
    const cookieConsent = document.cookie
      .split('; ')
      .find(row => row.startsWith('cookieConsent='));

    if (!cookieConsent) return true;

    const value = cookieConsent.split('=')[1];
    return value !== 'true' && value !== 'false';
  }
  function createCookieBanner() {
    const consentPopup = document.createElement('div');
    consentPopup.id = 'cookie-consent-popup';
    consentPopup.classList.add('cookie-card'); // 👈 используем CSS-класс вместо inline-стилей

    consentPopup.innerHTML = `
      <p class="cookieEmoji"> 🍪</p>
      <p class="cookieHeading">Мы используем cookie </p>
      <p class="cookieDescription">Для удобства пользователей на сайте мы используем cookie<br><a href="/privacy/#cookies">Подробнее - в Политике cookie</a>.</p>
      <div class="buttonContainer">
        <button id="cookie-accept" class="acceptButton">Принять</button>
        <button id="cookie-decline" class="declineButton">Отклонить</button>
      </div>
    `;

    document.body.appendChild(consentPopup);

    const acceptBtn = document.getElementById('cookie-accept');
    const declineBtn = document.getElementById('cookie-decline');

    acceptBtn.addEventListener('click', () => {
      saveCookieConsent(true);
      consentPopup.remove();
    });

    declineBtn.addEventListener('click', () => {
      saveCookieConsent(false);
      consentPopup.remove();
    });
  }

  // ✅ Показываем баннер, если нужно
  if (shouldShowCookieBanner()) {
    createCookieBanner();
  }
});
