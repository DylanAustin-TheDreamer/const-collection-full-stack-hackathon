(function(){
  // Theme toggle script — switches which Scheme CSS file is loaded and persists choice in localStorage
  const SCHEMES = [
    'css/Scheme-1.css',
    'css/Scheme-2.css',
    'css/Scheme-3.css',
    'css/Scheme-4.css',
    'css/Scheme-5.css',
    'css/Scheme-6.css',
    'css/Scheme-7.css',
    'css/Scheme-8.css'
  ];
  // Added schemes 9-13
  SCHEMES.push('css/Scheme-9.css','css/Scheme-10.css','css/Scheme-11.css','css/Scheme-12.css','css/Scheme-13.css');
  const STORAGE_KEY = 'constcollection:scheme';
  const schemeLinkId = 'scheme-link';

  function getSchemeIndex(name) {
    if (!name) return 0;
    const normalized = name.replace(/^\//, '').replace(/^css\//, 'css/');
    return SCHEMES.findIndex(s => s.endsWith(normalized)) || 0;
  }

  function applySchemeByHref(href) {
    const link = document.getElementById(schemeLinkId);
    if (!link) return;
    // If href is already absolute/static, just set it
    link.setAttribute('href', href.startsWith('/') ? href : ('{% static "' + href + '" %}' ));
  }

  function setSchemeByName(name) {
    // name may be 'Scheme-1.css' or 'css/Scheme-1.css'
    let target = name;
    if (!name.startsWith('css/')) {
      target = 'css/' + name;
    }
    const link = document.getElementById(schemeLinkId);
    if (!link) return;
    // Build static URL relative to Django static mapping: we assume static files are served from /static/
    // Use a simple path replacement so the href points at /static/css/... in production.
    link.href = window.STATIC_URL ? (window.STATIC_URL + target.replace(/^css\//, 'css/')) : ('/static/' + target);
    try { localStorage.setItem(STORAGE_KEY, target); } catch(e){}
  }

  function getSavedScheme() {
    try { return localStorage.getItem(STORAGE_KEY); } catch(e) { return null; }
  }

  function applySavedOrDefault() {
    const saved = getSavedScheme();
    const link = document.getElementById(schemeLinkId);
    if (!link) return;
    if (saved) {
      link.href = window.STATIC_URL ? (window.STATIC_URL + saved) : ('/static/' + saved);
    }
  }

  function cycleScheme() {
    const link = document.getElementById(schemeLinkId);
    if (!link) return;
    const current = (link.getAttribute('href') || '').split('/').pop();
    const idx = SCHEMES.findIndex(s => s.endsWith(current));
    const next = SCHEMES[(idx + 1) % SCHEMES.length];
    link.href = window.STATIC_URL ? (window.STATIC_URL + next) : ('/static/' + next);
    try { localStorage.setItem(STORAGE_KEY, next); } catch(e){}
  }

  // Expose to window for debugging and manual toggling
  window.ThemeToggle = {
    setScheme: setSchemeByName,
    cycleScheme: cycleScheme,
    applySaved: applySavedOrDefault
  };

  // Apply saved scheme on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function(){
    applySavedOrDefault();
  });
})();
