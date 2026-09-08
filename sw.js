---
layout: null
---
var CACHE_NAME = "pixyll2-{{site.time | date: '%Y%m%d%H%M%S'}}";

self.addEventListener("install", function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll([
        "{{ '/css/pixyll.css' | relative_url }}?{{ site.time | date: '%Y%m%d%H%M' }}",
        "{{ '/' | relative_url }}"
      ]);
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

self.addEventListener("activate", function(e) {
  e.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.map(function(name) {
          if (name != CACHE_NAME) {
            return caches.delete(name);
          }
        })
      ).then(function() {
        return clients.claim();
      });
    })
  );
});

addEventListener("fetch", function(e) {
  if (e.request.mode === "navigate") {
    e.respondWith(
      fetch(e.request).catch(function() {
        return caches.match(e.request).then(function(response) {
          return response || caches.match("{{ '/' | relative_url }}");
        });
      })
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then(function(response) {
        return response || fetch(e.request).then(function(response) {
        var clonedResponse = response.clone();
        var hosts = [
          "https://fonts.googleapis.com",
          "https://fonts.gstatic.com",
          "https://maxcdn.bootstrapcdn.com",
          "https://cdnjs.cloudflare.com"
        ];
        hosts.map(function(host) {
          if (e.request.url.indexOf(host) === 0) {
            caches.open(CACHE_NAME).then(function(cache) {
              cache.put(e.request, clonedResponse);
            });
          }
        });
        return response;
      });
    })
  );
});
