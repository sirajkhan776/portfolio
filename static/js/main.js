document.addEventListener('DOMContentLoaded', () => {
  const prefersReduced = (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) || document.documentElement.getAttribute('data-reduce') === '1';

  // Reveal animations
  if (!prefersReduced) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });

    document.querySelectorAll('.reveal').forEach((el) => {
      if (!el.style.transitionDuration) el.style.transitionDuration = '600ms';
      observer.observe(el);
    });

    document.querySelectorAll('[data-stagger]')?.forEach((group) => {
      const step = parseInt(group.getAttribute('data-stagger') || '80', 10);
      const items = group.querySelectorAll('.reveal');
      items.forEach((item, i) => {
        item.style.transitionDelay = `${i * step}ms`;
      });
    });
  } else {
    // Reduced motion: show everything immediately
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('in-view'));
  }

  // User menu: click to toggle, click outside to close, Esc to close
  document.querySelectorAll('[data-user-menu]').forEach((menu) => {
    const toggle = menu.querySelector('[data-user-menu-toggle]');
    if (!toggle) return;
    const close = () => menu.classList.remove('open');
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      menu.classList.toggle('open');
    });
    const outsideClose = (e) => { if (!menu.contains(e.target)) close(); };
    document.addEventListener('pointerdown', outsideClose, { passive: true });
    document.addEventListener('click', outsideClose);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });
  });

  // Nav services menu: click to toggle on mobile, close on outside/Esc
  document.querySelectorAll('[data-nav-menu]').forEach((menu) => {
    const toggle = menu.querySelector('[data-nav-menu-toggle]');
    if (!toggle) return;
    const close = () => menu.classList.remove('open');
    toggle.addEventListener('click', (e) => {
      // Allow regular anchor behavior with Ctrl/Cmd click
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      menu.classList.toggle('open');
    });
    const outsideClose = (e) => { if (!menu.contains(e.target)) close(); };
    document.addEventListener('pointerdown', outsideClose, { passive: true });
    document.addEventListener('click', outsideClose);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });
  });

  // Mobile nav toggle
  const headerEl = document.querySelector('.site-header');
  const mobileBtn = document.querySelector('[data-mobile-nav-toggle]');
  if (headerEl && mobileBtn) {
    const closeNav = () => {
      headerEl.classList.remove('nav-open');
      try { mobileBtn.setAttribute('aria-expanded', 'false'); } catch(e) {}
    };
    mobileBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const next = !headerEl.classList.contains('nav-open');
      headerEl.classList.toggle('nav-open', next);
      try { mobileBtn.setAttribute('aria-expanded', next ? 'true' : 'false'); } catch(e) {}
    });
    // Close when clicking real navigation links (not submenu toggles)
    document.querySelectorAll('.primary-nav a:not([data-nav-menu-toggle])')
      .forEach((a) => a.addEventListener('click', closeNav));
    // Close on outside click
    const outsideHandler = (e) => {
      const nav = document.querySelector('.primary-nav');
      if (!nav) return;
      if (headerEl.classList.contains('nav-open') && !nav.contains(e.target) && !mobileBtn.contains(e.target)) {
        closeNav();
      }
    };
    // Use pointerdown for more reliable touch behavior, fallback to click
    document.addEventListener('pointerdown', outsideHandler, { passive: true });
    document.addEventListener('click', outsideHandler);
    // Close on Esc
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNav(); });
    // Close on hash change (after in-page navigation)
    window.addEventListener('hashchange', closeNav);
    // Close if resized to desktop
    window.addEventListener('resize', () => { if (window.innerWidth > 720) closeNav(); });
  }

  // Smooth scroll for in-page anchors
  const samePath = (href) => {
    try{ return new URL(href, window.location.origin).pathname === window.location.pathname; }catch{return false}
  };
  document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const href = link.getAttribute('href');
      const hash = href.startsWith('/#') ? href.slice(1) : href;
      const id = hash.slice(1);
      if (!id) return;
      if (href.startsWith('#') || (href.startsWith('/#') && samePath(href))) {
        const target = document.getElementById(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({behavior: 'smooth', block: 'start'});
          history.replaceState(null, '', `#${id}`);
        }
      }
    });
  });

  // Theme toggle
  const themeBtn = document.querySelector('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch(e) {}
    });
  }

  // Default section scroll on home
  try {
    const def = document.documentElement.getAttribute('data-default-section');
    const onHome = window.location.pathname === '/' || window.location.pathname.endsWith('/');
    const hasHash = !!window.location.hash;
    if (onHome && !hasHash && def && def !== 'home') {
      const map = {about: 'about', services: 'services', projects: 'projects', experience: 'experience', skills: 'skills'};
      const id = map[def];
      const el = id && document.getElementById(id);
      if (el) {
        setTimeout(() => el.scrollIntoView({behavior: 'smooth'}), 50);
      }
    }
  } catch(e) {}
});
