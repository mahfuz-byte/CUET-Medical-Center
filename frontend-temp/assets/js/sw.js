const CACHE_NAME = 'cmc-cache-v1';
const CORE_ASSETS = [
  './',
  './index.html',
  './about.html',
  './services.html',
  './doctors.html',
  './emergency.html',
  './contact.html',
  './notices.html',
  './alerts.html',
  './assistant.html',
  './medical-records.html',
  './donors.html',
  './roster.html',
  './offline.html',
  './assets/css/styles.css',
  './assets/js/app.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  // For navigation requests, try network first, fallback to cache then offline
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(() => caches.match(req).then((res) => res || caches.match('./offline.html')))
    );
    return;
  }
  // For other requests, try cache first, then network
  event.respondWith(
    caches.match(req).then((cached) => cached || fetch(req).then((res) => {
      const copy = res.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
      return res;
    }).catch(() => cached))
  );
});