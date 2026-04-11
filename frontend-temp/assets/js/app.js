// Simple client-side helpers
(function () {
  // API Configuration
  const API_BASE_URL = 'http://127.0.0.1:8000/api';

  // ===== AUTH STATE MANAGEMENT =====
  function checkAuthState() {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    return token && user ? { token, user: JSON.parse(user) } : null;
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    updateNavbar();
    // Detect if on nested page and use correct path
    const isNestedPage = window.location.pathname.includes('/student/');
    const indexPath = isNestedPage ? '../index.html' : 'index.html';
    window.location.href = indexPath;
  }

  function updateNavbar() {
    const auth = checkAuthState();
    // Find login button with flexible path matching (login.html or ../login.html)
    const loginBtn = document.querySelector('a.btn-primary[href*="login"]') || 
                     document.querySelector('a[href*="login.html"]');
    
    if (!loginBtn) return; // Navbar not loaded yet

    const navMenu = loginBtn.closest('.top-nav') || loginBtn.parentElement;
    const isNestedPage = window.location.pathname.includes('/student/');
    const profilePath = isNestedPage ? `../profile-${auth ? auth.user.role : 'student'}.html` : `profile-${auth ? auth.user.role : 'student'}.html`;

    if (auth) {
      // User is logged in
      const user = auth.user;
      
      // Remove login button if exists
      const existingLoginBtn = navMenu.querySelector('a[href*="login"]');
      if (existingLoginBtn && existingLoginBtn.textContent.toLowerCase() === 'login') {
        existingLoginBtn.remove();
      }

      // Add dashboard button
      let dashboardLink = navMenu.querySelector('a[href*="dashboard"]');
      if (!dashboardLink) {
        dashboardLink = document.createElement('a');
        if (isNestedPage) {
          dashboardLink.href = '#'; // Don't navigate from nested pages
        } else {
          // Map role to dashboard file
          const dashboardMap = {
            'student': 'student/dashboard.html',
            'doctor': 'doctor.html',
            'admin': 'admin.html'
          };
          dashboardLink.href = dashboardMap[user.role] || 'index.html';
        }
        dashboardLink.className = 'nav-link';
        dashboardLink.textContent = 'Dashboard';
        navMenu.appendChild(dashboardLink);
      }

      // Add profile link
      let profileLink = navMenu.querySelector('a[href*="profile"]');
      if (!profileLink) {
        profileLink = document.createElement('a');
        profileLink.href = isNestedPage ? `../profile-${user.role}.html` : `profile-${user.role}.html`;
        profileLink.className = 'nav-link';
        profileLink.textContent = 'Profile';
        navMenu.appendChild(profileLink);
      }

      let logoutBtn = navMenu.querySelector('a.logout-btn');
      if (!logoutBtn) {
        logoutBtn = document.createElement('a');
        logoutBtn.href = '#';
        logoutBtn.className = 'btn btn-primary logout-btn';
        logoutBtn.textContent = 'Logout';
        logoutBtn.addEventListener('click', (e) => {
          e.preventDefault();
          logout();
        });
        navMenu.appendChild(logoutBtn);
      }
    } else {
      // User is not logged in
      const dashboardLink = navMenu.querySelector('a[href*="dashboard"]');
      const profileLink = navMenu.querySelector('a[href*="profile"]');
      const logoutBtn = navMenu.querySelector('a.logout-btn');
      
      if (dashboardLink) dashboardLink.remove();
      if (profileLink) profileLink.remove();
      if (logoutBtn) logoutBtn.remove();

      // Ensure login button exists
      const hasLogin = navMenu.querySelector('a[href*="login"]');
      if (!hasLogin) {
        const newLoginBtn = document.createElement('a');
        newLoginBtn.href = isNestedPage ? '../login.html' : 'login.html';
        newLoginBtn.className = 'btn btn-primary';
        newLoginBtn.textContent = 'Login';
        navMenu.appendChild(newLoginBtn);
      }
    }
  }

  // Update navbar when page loads
  window.addEventListener('DOMContentLoaded', updateNavbar);
  
  // Check auth state periodically (every 5 seconds when user interacts)
  window.addEventListener('focus', updateNavbar);

  // ===== LEGACY LOGIN HANDLER (keep for backward compatibility) =====
  var form = document.getElementById('loginForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var role = (document.querySelector('input[name="role"]:checked') || {}).value;
      var userId = document.getElementById('userId').value.trim();
      var password = document.getElementById('password').value.trim();

      if (!role) {
        if (window.showToast) window.showToast('Please select a role.', 'warning');
        return;
      }

      if (!userId || !password) {
        if (window.showToast) window.showToast('Please enter email and password.', 'warning');
        return;
      }

      var submitBtn = form.querySelector('button[type="submit"]');
      var originalText = submitBtn ? submitBtn.textContent : 'Login';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Logging in...';
      }

      fetch(API_BASE_URL + '/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: userId, password: password })
      })
        .then(function (response) {
          if (!response.ok) {
            return response.json().then(function (data) {
              throw new Error(data.detail || 'Invalid credentials');
            });
          }
          return response.json();
        })
        .then(function (data) {
          localStorage.setItem('accessToken', data.access);
          localStorage.setItem('refreshToken', data.refresh);
          return fetch(API_BASE_URL + '/auth/me/', {
            headers: { 'Authorization': 'Bearer ' + data.access }
          });
        })
        .then(function (response) {
          if (!response.ok) throw new Error('Failed to get user profile');
          return response.json();
        })
        .then(function (user) {
          if (user.role !== role) {
            throw new Error('Selected role does not match your account role');
          }
          localStorage.setItem('currentUser', JSON.stringify(user));
          if (window.showToast) {
            window.showToast('Welcome ' + (user.first_name || user.email) + '!', 'success');
          }
          setTimeout(function () {
            if (user.role === 'admin') {
              window.location.href = 'admin.html';
            } else if (user.role === 'student') {
              window.location.href = 'student/dashboard.html';
            } else if (user.role === 'doctor') {
              window.location.href = 'doctor.html';
            }
          }, 500);
        })
        .catch(function (error) {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
          }
          if (window.showToast) {
            window.showToast(error.message || 'Login failed. Please try again.', 'error');
          }
          console.error('Login error:', error);
        });
    });
  }

  var menuBtn = document.getElementById('menuToggle');
  var topNav = document.getElementById('topNav');
  function closeMenu() {
    if (!menuBtn || !topNav) return;
    topNav.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }
  if (menuBtn && topNav) {
    menuBtn.addEventListener('click', function () {
      var isOpen = topNav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(isOpen));
      if (isOpen) {
        // Focus first link for accessibility
        var firstLink = topNav.querySelector('a');
        if (firstLink) setTimeout(function () { firstLink.focus(); }, 0);
      }
    });
    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!topNav.classList.contains('open')) return;
      var within = topNav.contains(e.target) || menuBtn.contains(e.target);
      if (!within) closeMenu();
    });
    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
    // Close when a nav link is clicked
    topNav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });
  }

  // Smooth scroll for in-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
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
    var observer = new MutationObserver(function () {
      chat.scrollTop = chat.scrollHeight;
    });
    observer.observe(chat, { childList: true });
  }

  // Login: show password toggle
  var showPw = document.getElementById('showPassword');
  var pwInput = document.getElementById('password');
  if (showPw && pwInput) {
    showPw.addEventListener('change', function () {
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
    sidebarToggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('sidebar-open');
      sidebarToggle.setAttribute('aria-expanded', String(open));
    });
    // Close when clicking overlay (captured on document)
    document.addEventListener('click', function (e) {
      if (!document.body.classList.contains('sidebar-open')) return;
      var within = sidebar.contains(e.target) || sidebarToggle.contains(e.target);
      if (!within) closeSidebar();
    });
    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeSidebar();
    });
    // Close on nav click
    sidebar.addEventListener('click', function (e) {
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
    setTimeout(function () {
      t.style.opacity = '0'; t.style.transform = 'translateY(-6px)';
      setTimeout(function () { t.remove(); }, 200);
    }, 2500);
  }
  window.showToast = showToast;

  // Back to top button
  (function () {
    var btn = document.createElement('button');
    btn.className = 'back-to-top btn';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Back to top');
    btn.textContent = '↑ Top';
    document.body.appendChild(btn);
    function onScroll() {
      if (window.scrollY > 300) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  })();

  // Theme toggle with persistence
  (function () {
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
    document.addEventListener('DOMContentLoaded', function () { document.body.appendChild(btn); });
    var current = getPreferredTheme();
    applyTheme(current);
    btn.addEventListener('click', function () {
      current = (current === 'light') ? 'dark' : 'light';
      localStorage.setItem(storageKey, current);
      applyTheme(current);
    });
    // React to system theme changes when no explicit user preference
    if (!localStorage.getItem(storageKey) && window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function (e) {
        current = e.matches ? 'light' : 'dark';
        applyTheme(current);
      });
    }
  })();

  // Roster: load and render from JSON with skeleton + fallback
  (function () {
    var docList = document.getElementById('doctor-list');
    var ambList = document.getElementById('ambulance-list');
    if (!docList && !ambList) return;
    function skeleton(count) {
      return new Array(count).fill(0).map(function () { return '<div class="item skeleton" style="height:48px;"></div>'; }).join('');
    }
    if (docList) { docList.setAttribute('aria-busy', 'true'); docList.innerHTML = skeleton(3); }
    if (ambList) { ambList.setAttribute('aria-busy', 'true'); ambList.innerHTML = skeleton(2); }
    Promise.all([
      fetch(API_BASE_URL + '/roster/doctors/').then(r => r.json()).catch(e => []),
      fetch(API_BASE_URL + '/roster/ambulances/').then(r => r.json()).catch(e => [])
    ]).then(function ([doctors, ambulances]) {
      if (docList) {
        docList.innerHTML = doctors.length ? doctors.map(function (d) {
          return '<div class="item">\n'
            + '  <div class="item-title">' + (d.name || 'Unknown') + ' — ' + (d.dept || '') + '</div>\n'
            + '  <div class="item-meta">' + (d.title || '') + ' | ' + (d.hours || '') + '</div>\n'
            + '</div>';
        }).join('') : '<div class="item">No doctors listed.</div>';
        docList.removeAttribute('aria-busy');
      }
      if (ambList) {
        ambList.innerHTML = ambulances.length ? ambulances.map(function (a) {
          return '<div class="item">\n'
            + '  <div class="item-title">' + (a.ambulance_id || 'Ambulance') + '</div>\n'
            + '  <div class="item-meta">Status: ' + (a.status || 'Unknown') + ' | ' + (a.contact || '') + '</div>\n'
            + '</div>';
        }).join('') : '<div class="item">No ambulances listed.</div>';
        ambList.removeAttribute('aria-busy');
      }
    });
  })();

  // Student/Doctor portal: dedicated roster and availability panels
  (function(){
    var doctorOnlyList = document.getElementById('doctor-roster-list');
    var ambulanceOnlyList = document.getElementById('ambulance-roster-list');
    var testKitList = document.getElementById('availability-testkits');
    var bedList = document.getElementById('availability-beds');
    var medicineList = document.getElementById('availability-medicines');

    if (!doctorOnlyList && !ambulanceOnlyList && !testKitList && !bedList && !medicineList) return;

    function authHeaders() {
      var token = localStorage.getItem('accessToken');
      return token ? { 'Authorization': 'Bearer ' + token } : {};
    }

    function renderNotLoggedIn(el, label) {
      if (!el) return;
      el.innerHTML = '<div class="item">Login required to view ' + label + '.</div>';
    }

    function loadDoctorsOnly() {
      if (!doctorOnlyList) return;
      doctorOnlyList.innerHTML = '<div class="item">Loading doctor roster...</div>';
      fetch(API_BASE_URL + '/roster/doctors/')
        .then(function(r){ return r.ok ? r.json() : []; })
        .then(function(doctors){
          doctorOnlyList.innerHTML = doctors.length ? doctors.map(function(d){
            return '<div class="item">'
              + '<div class="item-title">' + (d.name || 'Unknown') + '</div>'
              + '<div class="item-meta">Department: ' + (d.dept || '-') + '</div>'
              + '<div class="item-meta">Title: ' + (d.title || '-') + '</div>'
              + '<div class="item-meta">Hours: ' + (d.hours || '-') + '</div>'
              + '</div>';
          }).join('') : '<div class="item">No doctors listed.</div>';
        })
        .catch(function(){
          doctorOnlyList.innerHTML = '<div class="item">Unable to load doctor roster.</div>';
        });
    }

    function loadAmbulancesOnly() {
      if (!ambulanceOnlyList) return;
      ambulanceOnlyList.innerHTML = '<div class="item">Loading ambulance roster...</div>';
      fetch(API_BASE_URL + '/roster/ambulances/')
        .then(function(r){ return r.ok ? r.json() : []; })
        .then(function(ambulances){
          ambulanceOnlyList.innerHTML = ambulances.length ? ambulances.map(function(a){
            return '<div class="item">'
              + '<div class="item-title">' + (a.ambulance_id || 'Ambulance') + '</div>'
              + '<div class="item-meta">Status: ' + (a.status || 'Unknown') + '</div>'
              + '<div class="item-meta">Contact: ' + (a.contact || '-') + '</div>'
              + '</div>';
          }).join('') : '<div class="item">No ambulances listed.</div>';
        })
        .catch(function(){
          ambulanceOnlyList.innerHTML = '<div class="item">Unable to load ambulance roster.</div>';
        });
    }

    function loadAvailability() {
      var token = localStorage.getItem('accessToken');
      if (!token) {
        renderNotLoggedIn(testKitList, 'test kit availability');
        renderNotLoggedIn(bedList, 'bed availability');
        renderNotLoggedIn(medicineList, 'pharmacy availability');
        return;
      }

      if (testKitList) testKitList.innerHTML = '<div class="item">Loading test kits...</div>';
      if (bedList) bedList.innerHTML = '<div class="item">Loading bed availability...</div>';
      if (medicineList) medicineList.innerHTML = '<div class="item">Loading medicines...</div>';

      fetch(API_BASE_URL + '/records/inventory/', { headers: authHeaders() })
        .then(function(r){ return r.ok ? r.json() : []; })
        .then(function(items){
          var kits = items.filter(function(i){ return i.item_type === 'kit'; });
          var beds = items.filter(function(i){ return i.item_type === 'bed'; });

          if (testKitList) {
            testKitList.innerHTML = kits.length ? kits.map(function(k){
              return '<div class="item">'
                + '<div class="item-title">' + (k.name || 'Test Kit') + '</div>'
                + '<div class="item-meta">Available: ' + (k.quantity || 0) + '</div>'
                + '</div>';
            }).join('') : '<div class="item">No test kit data available.</div>';
          }

          if (bedList) {
            if (beds.length) {
              var totalBeds = beds.reduce(function(sum, b){ return sum + (Number(b.quantity) || 0); }, 0);
              bedList.innerHTML = '<div class="item"><div class="item-title">Available Beds</div><div class="item-meta">' + totalBeds + '</div></div>';
            } else {
              bedList.innerHTML = '<div class="item">No bed availability data available.</div>';
            }
          }
        })
        .catch(function(){
          if (testKitList) testKitList.innerHTML = '<div class="item">Unable to load test kit availability.</div>';
          if (bedList) bedList.innerHTML = '<div class="item">Unable to load bed availability.</div>';
        });

      fetch(API_BASE_URL + '/records/medicines/', { headers: authHeaders() })
        .then(function(r){ return r.ok ? r.json() : []; })
        .then(function(medicines){
          if (!medicineList) return;
          medicineList.innerHTML = medicines.length ? medicines.map(function(m){
            return '<div class="item">'
              + '<div class="item-title">' + (m.name || 'Medicine') + '</div>'
              + '<div class="item-meta">Dosage: ' + (m.dosage || '-') + '</div>'
              + '</div>';
          }).join('') : '<div class="item">No medicines available.</div>';
        })
        .catch(function(){
          if (medicineList) medicineList.innerHTML = '<div class="item">Unable to load pharmacy availability.</div>';
        });
    }

    loadDoctorsOnly();
    loadAmbulancesOnly();
    loadAvailability();
  })();

  // Highlight active top navigation link
  (function () {
    var nav = document.getElementById('topNav');
    if (!nav) return;
    var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    var links = nav.querySelectorAll('a.nav-link');
    links.forEach(function (a) {
      try {
        var target = (a.getAttribute('href') || '').split('/').pop().toLowerCase();
        if (target && here === target) {
          a.classList.add('active');
          a.setAttribute('aria-current', 'page');
        }
      } catch (_) { }
    });
  })();
})();
