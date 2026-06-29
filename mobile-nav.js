/**
 * Hymuebles Mobile Navigation — shared script
 * Fixes: hamburger toggle + touch submenu access
 */
(function() {
  var toggle = document.getElementById('menuToggle');
  var nav = document.getElementById('navLinks');
  if (!toggle || !nav) return;

  // ── 1. Hamburger toggle ──
  function openMenu() {
    nav.classList.add('open');
    toggle.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    nav.classList.remove('open');
    toggle.classList.remove('open');
    document.body.style.overflow = '';
    // Collapse all submenus
    nav.querySelectorAll('.nav-item.open').forEach(function(it) { it.classList.remove('open'); });
  }

  toggle.addEventListener('click', function(e) {
    e.stopPropagation();
    nav.classList.contains('open') ? closeMenu() : openMenu();
  });
  // Also bind touchend for iOS
  toggle.addEventListener('touchend', function(e) {
    e.preventDefault();
    e.stopPropagation();
    nav.classList.contains('open') ? closeMenu() : openMenu();
  });

  // ── 2. Close menu on outside tap ──
  document.addEventListener('click', function(e) {
    if (nav.classList.contains('open') && !nav.contains(e.target) && e.target !== toggle && !toggle.contains(e.target)) {
      closeMenu();
    }
  });

  // ── 3. Mobile dropdown toggle (chevron click) ──
  nav.querySelectorAll('.nav-item').forEach(function(item) {
    var link = item.querySelector(':scope > .nav-link');
    var drop = item.querySelector(':scope > .nav-dropdown');
    if (!link || !drop) return;

    // On mobile: chevron = toggle submenu, text = navigate
    link.addEventListener('click', function(e) {
      if (window.innerWidth <= 900) {
        // Was the click on the chevron SVG?
        var chevron = link.querySelector('.nav-chevron');
        if (chevron && (e.target === chevron || chevron.contains(e.target))) {
          e.preventDefault();
          e.stopPropagation();
          item.classList.toggle('open');
        }
        // else: let the link navigate normally (parent page)
      }
    });
  });

  // ── 4. Close menu when a dropdown item link is clicked ──
  nav.querySelectorAll('.nav-dropdown-item').forEach(function(di) {
    di.addEventListener('click', function() {
      if (window.innerWidth <= 900) { closeMenu(); }
    });
  });

  // ── 5. Scroll shadow ──
  var navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', function() {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }
})();
