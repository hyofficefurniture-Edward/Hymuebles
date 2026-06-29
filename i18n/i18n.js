(function () {
  'use strict';

  /* ------------------------------------------------------------------ */
  /*  Hongye Furniture – i18n module                                     */
  /*  Loads locale JSON, exposes t() / setLang() / currentLang,          */
  /*  and auto-renders [data-i18n] elements on DOMContentLoaded.         */
  /* ------------------------------------------------------------------ */

  var translations = {};
  var lang = 'es'; // default Latin American Spanish

  /* -- helpers -- */

  function getLangFromUrl() {
    var m = location.search.match(/[?&]lang=([a-z]{2})(?:&|$)/i);
    return m ? m[1].toLowerCase() : null;
  }

  function resolveLang() {
    // 1. URL query param  →  2. localStorage  →  3. default 'es'
    var fromUrl = getLangFromUrl();
    if (fromUrl && (fromUrl === 'es' || fromUrl === 'en')) return fromUrl;
    try {
      var stored = localStorage.getItem('hongye-lang');
      if (stored && (stored === 'es' || stored === 'en')) return stored;
    } catch (_) {}
    return 'es';
  }

  function setDocumentLang(l) {
    var html = document.documentElement;
    if (html) html.setAttribute('lang', l);
  }

  function setPageTitle() {
    var val = getNested(translations, 'page.title');
    if (val) document.title = val;
  }

  /* safely get a dot-separated key from translations object */
  function getNested(obj, path) {
    if (!obj || !path) return '';
    return path.split('.').reduce(function (acc, k) {
      return acc && acc[k] !== undefined ? acc[k] : '';
    }, obj);
  }

  /* -- public API attached to window.i18n -- */

  /** Look up a translation by dot-notation key */
  function t(key) {
    return getNested(translations, key) || key;
  }

  /** Switch language, persist, and re-render */
  function setLang(newLang) {
    if (newLang !== 'es' && newLang !== 'en') return;
    lang = newLang;
    try { localStorage.setItem('hongye-lang', newLang); } catch (_) {}
    loadAndRender();
  }

  /** Get the current language code */
  function currentLang() {
    return lang;
  }

  /* -- rendering -- */

  function renderAll() {
    setDocumentLang(lang);
    setPageTitle();

    // data-i18n  → textContent
    var els = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var key = el.getAttribute('data-i18n');
      if (key) el.textContent = t(key);
    }

    // data-i18n-html  → innerHTML
    els = document.querySelectorAll('[data-i18n-html]');
    for (i = 0; i < els.length; i++) {
      var elh = els[i];
      var keyh = elh.getAttribute('data-i18n-html');
      if (keyh) elh.innerHTML = t(keyh);
    }

    // data-i18n-placeholder  → placeholder attribute
    els = document.querySelectorAll('[data-i18n-placeholder]');
    for (i = 0; i < els.length; i++) {
      var elp = els[i];
      var keyp = elp.getAttribute('data-i18n-placeholder');
      if (keyp) elp.setAttribute('placeholder', t(keyp));
    }
  }

  /* -- load JSON & render -- */

  function loadAndRender() {
    var url = 'i18n/locales/' + lang + '.json';
    fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error('Failed to load locale: ' + lang);
        return res.json();
      })
      .then(function (data) {
        translations = data;
        renderAll();
        document.documentElement.classList.add('i18n-ready');
      })
      .catch(function (err) {
        console.error('[i18n] ' + err.message);
        // fallback: try English if Spanish fails
        if (lang === 'es') {
          lang = 'en';
          loadAndRender();
        }
      });
  }

  /* -- boot -- */

  lang = resolveLang();

  // Expose public API
  window.i18n = {
    t: t,
    setLang: setLang,
    currentLang: currentLang
  };

  // Start loading immediately; re-render on DOMContentLoaded as safety net
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      if (!translations || Object.keys(translations).length === 0) {
        loadAndRender();
      } else {
        renderAll();
      }
    });
  }

  // Also fire immediately in case script loads after DOM is ready
  loadAndRender();

})();
