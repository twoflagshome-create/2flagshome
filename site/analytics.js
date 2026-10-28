/* Google Analytics (GA4) com aviso de cookies.
   O Analytics só é carregado depois de a pessoa carregar em "Aceitar".
   A escolha fica guardada no navegador; para voltar a perguntar: link com data-cookies. */
(function () {
  var ID = "G-3X3W94WRQM";
  var CHAVE = "cookies-2flagshome";
  var lang = (document.documentElement.lang || "pt").slice(0, 2);
  var TXT = {
    pt: ["Usamos cookies do Google Analytics para perceber como o site é usado e melhorá-lo. Aceita?", "Aceitar", "Recusar"],
    en: ["We use Google Analytics cookies to understand how the site is used and improve it. Is that OK?", "Accept", "Decline"],
    fr: ["Nous utilisons les cookies de Google Analytics pour comprendre l'usage du site et l'améliorer. D'accord ?", "Accepter", "Refuser"]
  }[lang] || null;
  TXT = TXT || ["We use Google Analytics cookies to understand how the site is used and improve it. Is that OK?", "Accept", "Decline"];

  function ler() { try { return localStorage.getItem(CHAVE); } catch (e) { return null; } }
  function guardar(v) { try { localStorage.setItem(CHAVE, v); } catch (e) {} }

  var ativo = false;
  function carregar() {
    if (ativo) return;
    ativo = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", ID, { anonymize_ip: true });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
    document.head.appendChild(s);
  }
  function evento(nome, dados) { if (ativo) gtag("event", nome, dados || {}); }

  // Contactos: pedidos pelos formulários, WhatsApp, telefone e email
  document.addEventListener("submit", function (e) {
    var f = e.target;
    if (f && f.getAttribute("data-netlify")) evento("generate_lead", { form_name: f.getAttribute("name"), page_language: lang });
  }, true);
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var h = a.getAttribute("href");
    if (h.indexOf("wa.me/") > -1) evento("contact_whatsapp", { page_language: lang });
    else if (h.indexOf("tel:") === 0) evento("contact_phone", { page_language: lang });
    else if (h.indexOf("mailto:") === 0) evento("contact_email", { page_language: lang });
    if (a.hasAttribute("data-cookies")) { e.preventDefault(); aviso(); }
  }, true);

  function aviso() {
    if (document.getElementById("aviso-cookies")) return;
    var d = document.createElement("div");
    d.id = "aviso-cookies";
    d.setAttribute("role", "dialog");
    d.setAttribute("aria-label", "Cookies");
    d.style.cssText = "position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;max-width:560px;margin:0 auto;background:#F7F5F0;color:#2A1A1E;border:1px solid #B08A3E;box-shadow:0 8px 30px rgba(42,26,30,.18);padding:18px 20px;font:14px/1.5 Montserrat,Arial,sans-serif;display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center";
    var p = document.createElement("p");
    p.style.cssText = "margin:0;flex:1 1 260px";
    p.textContent = TXT[0];
    var bs = document.createElement("div");
    bs.style.cssText = "display:flex;gap:8px";
    [[TXT[2], "nao", "transparent", "#6B1E2E"], [TXT[1], "sim", "#6B1E2E", "#F7F5F0"]].forEach(function (b) {
      var x = document.createElement("button");
      x.type = "button";
      x.textContent = b[0];
      x.style.cssText = "cursor:pointer;font:600 12px Montserrat,Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:10px 16px;border:1px solid #6B1E2E;background:" + b[2] + ";color:" + b[3];
      x.onclick = function () { guardar(b[1]); d.remove(); if (b[1] === "sim") carregar(); };
      bs.appendChild(x);
    });
    d.appendChild(p);
    d.appendChild(bs);
    document.body.appendChild(d);
  }

  var escolha = ler();
  if (escolha === "sim") carregar();
  else if (escolha !== "nao") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", aviso);
    else aviso();
  }
})();
