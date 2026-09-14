// Retirement worker for the old Pixyll cache-first service worker.
// Keep this file temporarily so browsers with the old worker installed can
// receive the update, clear stale caches, and unregister it.
self.addEventListener('install', function () {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil((async function () {
    var cacheNames = await caches.keys();
    await Promise.all(cacheNames.map(function (cacheName) {
      return caches.delete(cacheName);
    }));

    await self.registration.unregister();

    var windows = await self.clients.matchAll({ type: 'window' });
    windows.forEach(function (client) {
      client.navigate(client.url);
    });
  })());
});
