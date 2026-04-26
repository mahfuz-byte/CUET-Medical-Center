// Simple client-side helpers
(function() {
  // Hardcoded admin credentials
  const ADMIN_CREDENTIALS = {
    username: 'admin',
    password: 'admin123'
  };

  // Handle login role redirect
  var form = document.getElementById('loginForm');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var role = (document.querySelector('input[name="role"]:checked') || {}).value;
      var userId = document.getElementById('userId').value.trim();
      var password = document.getElementById('password').value.trim();
      
      if (!role) {
        if (window.showToast) window.showToast('Please select a role.', 'warning');
        return;
      }

      // Admin login validation
      if (role === 'admin') {
        if (userId === ADMIN_CREDENTIALS.username && password === ADMIN_CREDENTIALS.password) {
          localStorage.setItem('currentUser', JSON.stringify({ role: 'admin', username: userId }));
          if (window.showToast) window.showToast('Welcome Admin!', 'success');
          window.location.href = 'admin.html';
        } else {
          if (window.showToast) window.showToast('Invalid admin credentials.', 'warning');
        }
        return;
      }

      if (window.showToast) window.showToast('Signing in (demo)...', 'success');
      localStorage.setItem('currentUser', JSON.stringify({ role: role, username: userId }));
      
      if (role === 'student') {
        window.location.href = 'student/dashboard.html';
      } else if (role === 'doctor') {
        // Redirect to existing doctors page in this workspace
        window.location.href = 'student/doctors.html';
      }
    });
  }

  // Responsive menu toggle
  var menuBtn = document.getElementById('menuToggle');
  var topNav = document.getElementById('topNav');
  function closeMenu() {
    if (!menuBtn || !topNav) return;
    topNav.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }
  if (menuBtn && topNav) {
    menuBtn.addEventListener('click', function() {
      var isOpen = topNav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(isOpen));
      if (isOpen) {
        // Focus first link for accessibility
        var firstLink = topNav.querySelector('a');
        if (firstLink) setTimeout(function(){ firstLink.focus(); }, 0);
      }
    });
    // Close on outside click
    document.addEventListener('click', function(e) {
      if (!topNav.classList.contains('open')) return;
      var within = topNav.contains(e.target) || menuBtn.contains(e.target);
      if (!within) closeMenu();
    });
    // Close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMenu();
    });
    // Close when a nav link is clicked
    topNav.addEventListener('click', function(e) {
      if (e.target.closest('a')) closeMenu();
    });
  }

  // Smooth scroll for in-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(function(a){
    a.addEventListener('click', function(e){
      var id = a.getAttribute('href').slice(1);
      if (!id) return;
      var target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Assistant chat: auto-scroll to newest message
  var chat = document.getElementById('assistant-chat');
  if (chat) {
    var observer = new MutationObserver(function(){
      chat.scrollTop = chat.scrollHeight;
    });
    observer.observe(chat, { childList: true });
  }

  // Login: show password toggle
  var showPw = document.getElementById('showPassword');
  var pwInput = document.getElementById('password');
  if (showPw && pwInput) {
    showPw.addEventListener('change', function(){
      pwInput.type = showPw.checked ? 'text' : 'password';
      pwInput.focus();
    });
  }

  // Student dashboard: sidebar drawer toggle
  var sidebarToggle = document.querySelector('.sidebar-toggle');
  var sidebar = document.getElementById('sidebar');
  if (sidebarToggle && sidebar) {
    function openSidebar() {
      document.body.classList.add('sidebar-open');
      sidebarToggle.setAttribute('aria-expanded', 'true');
    }
    function closeSidebar() {
      document.body.classList.remove('sidebar-open');
      sidebarToggle.setAttribute('aria-expanded', 'false');
    }
    sidebarToggle.addEventListener('click', function(){
      var open = document.body.classList.toggle('sidebar-open');
      sidebarToggle.setAttribute('aria-expanded', String(open));
    });
    // Close when clicking overlay (captured on document)
    document.addEventListener('click', function(e){
      if (!document.body.classList.contains('sidebar-open')) return;
      var within = sidebar.contains(e.target) || sidebarToggle.contains(e.target);
      if (!within) closeSidebar();
    });
    // Close on Escape
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') closeSidebar();
    });
    // Close on nav click
    sidebar.addEventListener('click', function(e){
      if (e.target.closest('a')) closeSidebar();
    });
  }

  // Global toast notifications
  function ensureToastContainer() {
    var el = document.querySelector('.toast-container');
    if (!el) {
      el = document.createElement('div');
      el.className = 'toast-container';
      document.body.appendChild(el);
    }
    return el;
  }
  function showToast(message, type) {
    var container = ensureToastContainer();
    var t = document.createElement('div');
    t.className = 'toast' + (type ? (' ' + type) : '');
    t.setAttribute('role', 'status');
    t.setAttribute('aria-live', 'polite');
    t.textContent = message;
    container.appendChild(t);
    setTimeout(function(){
      t.style.opacity = '0'; t.style.transform = 'translateY(-6px)';
      setTimeout(function(){ t.remove(); }, 200);
    }, 2500);
  }
  window.showToast = showToast;

  // Back to top button
  (function(){
    var btn = document.createElement('button');
    btn.className = 'back-to-top btn';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Back to top');
    btn.textContent = '↑ Top';
    document.body.appendChild(btn);
    function onScroll(){
      if (window.scrollY > 300) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', function(){ window.scrollTo({ top: 0, behavior: 'smooth' }); });
  })();

  // Theme toggle with persistence
  (function(){
    var storageKey = 'theme';
    function ensureThemeMeta() {
      var meta = document.querySelector('meta[name="theme-color"]');
      if (!meta) {
        meta = document.createElement('meta');
        meta.name = 'theme-color';
        document.head.appendChild(meta);
      }
      return meta;
    }
    function applyTheme(theme) {
      var meta = ensureThemeMeta();
      if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        meta.setAttribute('content', '#ffffff');
      } else {
        document.documentElement.removeAttribute('data-theme');
        meta.setAttribute('content', '#0b1220');
      }
      if (btn) btn.setAttribute('aria-pressed', theme === 'light' ? 'true' : 'false');
      if (btn) btn.textContent = theme === 'light' ? '☀' : '🌙';
      if (btn) btn.title = theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme';
    }
    function getPreferredTheme() {
      var stored = localStorage.getItem(storageKey);
      if (stored === 'light' || stored === 'dark') return stored;
      var prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
      return prefersLight ? 'light' : 'dark';
    }
    var btn = document.createElement('button');
    btn.className = 'btn-icon theme-toggle-fixed';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Toggle theme');
    btn.setAttribute('aria-pressed', 'false');
    document.addEventListener('DOMContentLoaded', function(){ document.body.appendChild(btn); });
    var current = getPreferredTheme();
    applyTheme(current);
    btn.addEventListener('click', function(){
      current = (current === 'light') ? 'dark' : 'light';
      localStorage.setItem(storageKey, current);
      applyTheme(current);
    });
    // React to system theme changes when no explicit user preference
    if (!localStorage.getItem(storageKey) && window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function(e){
        current = e.matches ? 'light' : 'dark';
        applyTheme(current);
      });
    }
  })();

  // Roster: load and render from JSON with skeleton + fallback
  (function(){
    var docList = document.getElementById('doctor-list');
    var ambList = document.getElementById('ambulance-list');
    if (!docList && !ambList) return;
    function skeleton(count){
      return new Array(count).fill(0).map(function(){ return '<div class="item skeleton" style="height:48px;"></div>'; }).join('');
    }
    if (docList) { docList.setAttribute('aria-busy', 'true'); docList.innerHTML = skeleton(3); }
    if (ambList) { ambList.setAttribute('aria-busy', 'true'); ambList.innerHTML = skeleton(2); }
    fetch('assets/data/roster.json')
      .then(function(r){ if (!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
      .then(function(data){
        if (docList) {
          var docs = (data && data.doctors) || [];
          docList.innerHTML = docs.length ? docs.map(function(d){
            return '<div class="item">\n'
              + '  <div class="item-title">'+(d.name||'Unknown')+' — '+(d.dept||'')+'</div>\n'
              + '  <div class="item-meta">'+(d.title||'')+' | '+(d.hours||'')+'</div>\n'
              + '  <div>'+(d.bio||'')+'</div>\n'
              + '</div>';
          }).join('') : '<div class="item">No doctors listed.</div>';
          docList.removeAttribute('aria-busy');
        }
        if (ambList) {
          var ambs = (data && data.ambulances) || [];
          ambList.innerHTML = ambs.length ? ambs.map(function(a){
            return '<div class="item">\n'
              + '  <div class="item-title">'+(a.id||'Ambulance')+'</div>\n'
              + '  <div class="item-meta">Status: '+(a.status||'Unknown')+' | '+(a.contact||'')+'</div>\n'
              + '</div>';
          }).join('') : '<div class="item">No ambulances listed.</div>';
          ambList.removeAttribute('aria-busy');
        }
      })
      .catch(function(){
        if (docList) { docList.innerHTML = '<div class="item">Failed to load roster.</div>'; docList.removeAttribute('aria-busy'); }
        if (ambList) { ambList.innerHTML = '<div class="item">Failed to load roster.</div>'; ambList.removeAttribute('aria-busy'); }
      });
  })();

  // Highlight active top navigation link
  (function(){
    var nav = document.getElementById('topNav');
    if (!nav) return;
    var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    var links = nav.querySelectorAll('a.nav-link');
    links.forEach(function(a){
      try {
        var target = (a.getAttribute('href') || '').split('/').pop().toLowerCase();
        if (target && here === target) {
          a.classList.add('active');
          a.setAttribute('aria-current', 'page');
        }
      } catch(_){}
    });
  })();
})();
