document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-hamburger');
  const panel = document.querySelector('.mobile-panel');
  const setMenu = open => {
    panel.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  };
  toggle?.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  panel?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && panel?.classList.contains('open')) { setMenu(false); toggle.focus(); } });
  document.addEventListener('click', event => { if (!event.target.closest('.site-nav')) setMenu(false); });
  const mobile = matchMedia('(max-width: 800px)');
  mobile.addEventListener('change', () => { if (!mobile.matches) setMenu(false); });
  document.querySelectorAll('.acc-row').forEach((row, i) => {
    const button = row.querySelector('.acc-header');
    const region = row.querySelector('.acc-panel');
    region.id = `accordion-panel-${i}`;
    button.id = `accordion-button-${i}`;
    button.setAttribute('aria-controls', region.id);
    region.setAttribute('role', 'region');
    region.setAttribute('aria-labelledby', button.id);
    const sync = () => { const open = row.classList.contains('open'); button.setAttribute('aria-expanded', String(open)); region.inert = !open; };
    sync();
    button.addEventListener('click', () => { row.classList.toggle('open'); sync(); });
  });
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if (!reduced.matches && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('motion-ready');
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } }), { threshold: .08 });
    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
    reduced.addEventListener('change', () => { if (reduced.matches) document.documentElement.classList.remove('motion-ready'); });
  }
  const reportHeight = () => { if (window.parent !== window) window.parent.postMessage({ ilicheight: document.documentElement.scrollHeight }, '*'); };
  window.addEventListener('load', reportHeight);
  window.addEventListener('resize', reportHeight);
  if ('ResizeObserver' in window) new ResizeObserver(reportHeight).observe(document.body);
});
