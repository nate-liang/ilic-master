// ILIC site — shared behavior

document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav toggle
  const hamburger = document.querySelector('.nav-hamburger');
  const panel = document.querySelector('.mobile-panel');
  if (hamburger && panel) {
    hamburger.addEventListener('click', () => panel.classList.toggle('open'));
    panel.querySelectorAll('a').forEach(a => a.addEventListener('click', () => panel.classList.remove('open')));
  }

  // Staggered reveal for cards already in view (page is designed to fit one viewport, no scroll-trigger needed)
  document.querySelectorAll('[data-reveal]').forEach((el, i) => {
    el.style.animationDelay = `${Math.min(i * 0.06, 0.5)}s`;
  });
});

// Let a parent page know our height in case it wants to size the iframe.
// Pages are built to fill exactly 100dvh with no outer scroll, so this is
// a safety net only — it should rarely differ from the iframe's own height.
function reportHeight() {
  window.parent.postMessage({ ilicheight: document.documentElement.scrollHeight }, '*');
}
window.addEventListener('load', reportHeight);
window.addEventListener('resize', reportHeight);
