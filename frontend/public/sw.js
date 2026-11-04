const CACHE_NAME = 'php-shield-shell-v1';
const APP_SCOPE = new URL('./', self.registration.scope);
const APP_ICON = new URL('assets/drc-government-emblem.png', APP_SCOPE).href;
const APP_PWA_ICON = new URL('assets/app-icon.svg', APP_SCOPE).href;

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll([APP_SCOPE.href, APP_ICON, APP_PWA_ICON]))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key.startsWith('php-shield-') && key !== CACHE_NAME).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || !url.href.startsWith(APP_SCOPE.href)) return;

  // Inventory and security results may be sensitive; never cache API responses.
  if (url.pathname.includes('/api/v1/')) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => response)
        .catch(async () => (await caches.match(APP_SCOPE.href)) || Response.error())
    );
    return;
  }

  if (request.destination === 'script' || request.destination === 'style' || request.destination === 'image' || request.destination === 'font') {
    event.respondWith(
      caches.match(request).then((cached) => cached || fetch(request).then((response) => {
        if (response.ok) caches.open(CACHE_NAME).then((cache) => cache.put(request, response.clone()));
        return response;
      }))
    );
  }
});
