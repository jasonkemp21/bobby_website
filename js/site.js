/* Kennedy & Smith Mechanical */
(function () {
  var doc = document;

  // Book online: open the Housecall Pro window on the page when their script has loaded.
  // If it has not (blocked, slow, or this is the single-file preview) the link opens
  // the same booking page in a new tab, so the button always does something.
  doc.addEventListener('click', function (e) {
    var a = e.target.closest('[data-book]');
    if (a && window.HCPWidget && typeof window.HCPWidget.openModal === 'function') {
      e.preventDefault();
      window.HCPWidget.openModal();
    }
  });

  // phone menu
  var btn = doc.querySelector('.menu-btn');
  var nav = doc.getElementById('nav');
  function closeMenu() { if (nav) nav.classList.remove('open'); if (btn) btn.setAttribute('aria-expanded', 'false'); }
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) closeMenu(); });
  }

  // year in the footer
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // preview checklist
  var pv = doc.getElementById('pv');
  if (pv) {
    var opener = doc.querySelector('[data-pv-open]');
    var shut = function () { pv.hidden = true; if (opener) opener.focus(); };
    if (opener) opener.addEventListener('click', function () { pv.hidden = false; pv.querySelector('[data-pv-close]').focus(); });
    pv.addEventListener('click', function (e) { if (e.target === pv || e.target.closest('[data-pv-close]')) shut(); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !pv.hidden) shut(); });
  }

  // Single-file preview: every page is in this document; show one at a time by hash.
  if (doc.documentElement.hasAttribute('data-bundle')) {
    var pages = {};
    doc.querySelectorAll('[data-page]').forEach(function (el) { pages[el.getAttribute('data-page')] = el; });
    var groups = { plumbing: 'services', 'water-heaters': 'services', heating: 'services', 'air-conditioning': 'services', emergency: 'services', 'main-line': 'service-areas', 'delaware-county': 'service-areas', philadelphia: 'service-areas' };
    var show = function (slug, scroll) {
      if (!pages[slug]) slug = 'home';
      Object.keys(pages).forEach(function (k) { pages[k].classList.toggle('is-on', k === slug); });
      doc.title = pages[slug].getAttribute('data-title');
      var cur = groups[slug] || slug;
      doc.querySelectorAll('[data-nav]').forEach(function (a) {
        if (a.getAttribute('data-nav') === cur) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
      closeMenu();
      if (scroll) window.scrollTo(0, 0);
    };
    var fromHash = function () { return (location.hash || '').replace('#', '') || 'home'; };
    doc.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      var m = /^([a-z0-9-]+)\.html$/.exec(a.getAttribute('href'));
      if (!m) return;
      e.preventDefault();
      var slug = m[1] === 'index' ? 'home' : m[1];
      if (fromHash() === slug) { show(slug, true); return; }
      try { location.hash = slug; } catch (err) { /* hash not writable here */ }
      show(slug, true);
    });
    window.addEventListener('hashchange', function () { show(fromHash(), true); });
    show(fromHash(), false);
  }
})();
