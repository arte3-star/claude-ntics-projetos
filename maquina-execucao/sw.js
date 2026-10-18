// Máquina de Execução: guarda a página e a biblioteca do banco no celular para abrir sem internet.
// Os dados ficam em cópia local (a própria página cuida disso) e os envios esperam numa fila até o sinal voltar.
const CACHE = "mx-v2";
self.addEventListener("install", (e) => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then((c) => c.addAll(["./"]).catch(() => {}))); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
// rede com tempo limite: com sinal fraco, depois de 4 s abre a cópia guardada em vez de ficar presa
function redeComLimite(req, ms) {
  return new Promise((ok, falha) => { const t = setTimeout(() => falha(new Error("tempo")), ms);
    fetch(req).then((r) => { clearTimeout(t); ok(r); }, (e) => { clearTimeout(t); falha(e); }); }); }
self.addEventListener("fetch", (e) => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.hostname.endsWith("supabase.co") || url.hostname.endsWith("googleapis.com")) return;   // banco e Drive: sempre na rede
  if (req.mode === "navigate" || (url.origin === location.origin && url.pathname.endsWith("/"))) {
    e.respondWith(redeComLimite(req, 4000).then((r) => { if (r.ok) { const c = r.clone(); caches.open(CACHE).then((x) => x.put("./", c)); } return r; })
      .catch(() => caches.match("./").then((m) => m || fetch(req))));
    return; }
  if (url.hostname === "cdn.jsdelivr.net" || url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.match(req).then((m) => m || fetch(req).then((r) => { if (r.ok) { const c = r.clone(); caches.open(CACHE).then((x) => x.put(req, c)); } return r; }))); }
});
