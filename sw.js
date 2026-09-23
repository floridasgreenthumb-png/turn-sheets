/* Turn Sheets service worker — PUSH ONLY.
   Deliberately has NO fetch handler, so it never caches pages (no "stale until
   refresh" surprises); the auto-updater handles versions. Its only jobs are to
   receive a push and to open the right page when the notification is tapped. */
self.addEventListener("install", function(){ self.skipWaiting(); });
self.addEventListener("activate", function(e){ e.waitUntil(self.clients.claim()); });

self.addEventListener("push", function(e){
  var d = {};
  try{ d = e.data ? e.data.json() : {}; }catch(err){ d = {}; }
  var title = d.title || "New job posted";
  var opts = {
    body: d.body || "Open your turn sheets",
    icon: "icon-192.png",
    badge: "icon-192.png",
    tag: d.tag || "new-scope",
    renotify: true,
    data: { url: d.url || "/" }
  };
  e.waitUntil(self.registration.showNotification(title, opts));
});

self.addEventListener("notificationclick", function(e){
  e.notification.close();
  var url = (e.notification.data && e.notification.data.url) || "/";
  e.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function(list){
      for(var i = 0; i < list.length; i++){
        if(list[i].url.indexOf(url) >= 0 && "focus" in list[i]) return list[i].focus();
      }
      if(self.clients.openWindow) return self.clients.openWindow(url);
    })
  );
});
