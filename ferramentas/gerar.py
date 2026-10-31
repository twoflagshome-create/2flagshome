"""Gera as páginas dos imóveis (PT e EN), os cartões das páginas iniciais e o sitemap.

Uso (na pasta do repositório):  python3 ferramentas/gerar.py
Os dados estão em dados/imoveis.json e as fotos em site/imagens/.
As versões inglesa e francesa de cada imóvel ficam nos campos "en" e "fr" (as fotos e a ref. são as mesmas).
"""
import datetime
import html
import json
import pathlib
import re
import urllib.parse

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITE = RAIZ / "site"
DOMINIO = "https://2flagshome.com"
WHATSAPP = "351934263986"
FOTO_PADRAO = "liliana-retrato.jpg"
# Guias escritos à mão em site/en/guides/ e site/fr/guides/ (entram no sitemap, com as versões de cada língua)
GUIAS = [
    {"en": "/en/guides/buying-a-home-in-portugal", "fr": "/fr/guides/acheter-un-bien-au-portugal"},
    {"en": "/en/guides/buying-costs-in-portugal", "fr": "/fr/guides/frais-achat-immobilier-portugal"},
]

# Páginas de serviços escritas à mão em site/servicos/ (só em português, por agora)
SERVICOS = [
    {"pt": "/servicos/"},
    {"pt": "/servicos/melhorias-para-vender"},
]

COMO_CONHECEU = {
    "pt": ("Como me conheceu?", ["Pesquisa no Google", "Instagram", "Facebook", "LinkedIn", "Idealista ou outro portal", "Recomendação de alguém", "Outro"]),
    "en": ("How did you find me?", ["Google search", "Instagram", "Facebook", "LinkedIn", "Idealista or another property portal", "Someone recommended you", "Other"]),
    "fr": ("Comment m'avez-vous connue ?", ["Recherche Google", "Instagram", "Facebook", "LinkedIn", "Idealista ou un autre portail", "Sur recommandation", "Autre"]),
}

e = html.escape


def ref_txt(i):
    return f"Ref. {i['ref']}" if i.get("ref") else ""


def em_ingles(i):
    """O imóvel com os textos em inglês (fotos, ref. e links mantêm-se)."""
    return {**i, **i["en"]}


def em_frances(i):
    """O imóvel com os textos em francês (fotos, ref. e links mantêm-se)."""
    return {**i, **i["fr"]}


def url_pt(i):
    return f"/imoveis/{i['slug']}"


def url_en(i):
    return f"/en/homes/{i['en']['slug']}"


def url_fr(i):
    return f"/fr/biens/{i['fr']['slug']}"


def campo_como_conheceu(lingua, nome):
    rotulo, opcoes = COMO_CONHECEU[lingua]
    ops = "".join(f"<option>{e(o)}</option>" for o in opcoes)
    return f'<label class="full">{e(rotulo)}<select name="{nome}"><option value="">—</option>{ops}</select></label>'


def cartao(i, url=None, mais="Ver imóvel →", img="imagens/", negocio=None):
    url = url or url_pt(i)
    negocio = negocio or i["negocio"]
    spec = " · ".join(i["caracteristicas"])
    ref = f'<span class="ref">{e(ref_txt(i))}</span>' if i.get("ref") else ""
    if i.get("foto"):
        pos = f' style="object-position:{i["foto_posicao"]}"' if i.get("foto_posicao") else ""
        return (
            f'<article class="prop">\n'
            f' <a class="ph" href="{url}"><img src="{img}{e(i["foto"])}" alt="{e(i["alt"])}" loading="lazy"{pos}><span class="badge">{e(negocio)}</span></a>\n'
            f' <div class="pb"><p class="loc">{e(i["local"])}</p><h3><a href="{url}">{e(i["titulo"])}</a></h3><p class="spec">{e(spec)}</p>\n'
            f' <div class="pf"><span class="price">{e(i["preco"])}</span>{ref}</div>\n'
            f' <a class="more" href="{url}">{e(mais)}</a></div></article>'
        )
    return (
        f'<article class="prop plain"><div class="pb"><span class="badge static">{e(negocio)}</span>'
        f'<p class="loc">{e(i["local"])}</p><h3><a href="{url}">{e(i["titulo"])}</a></h3><p class="spec">{e(spec)}</p>'
        f'<div class="pf"><span class="price">{e(i["preco"])}</span>{ref}</div>'
        f'<a class="more" href="{url}">{e(mais)}</a></div></article>'
    )


def cartao_en(i):
    return cartao(em_ingles(i), url_en(i), "See this home →", "/imagens/")


def cartao_fr(i):
    return cartao(em_frances(i), url_fr(i), "Voir le bien →", "/imagens/")


def bloco_imagem(i):
    if i.get("foto"):
        pos = f' style="object-position:{i["foto_posicao"]}"' if i.get("foto_posicao") else ""
        return f'<figure class="im-foto"><img src="/imagens/{e(i["foto"])}" alt="{e(i["alt"])}"{pos}><span class="badge">{e(i["negocio"])}</span></figure>'
    return f'<div class="im-foto im-sem-foto"><span class="badge">{e(i["negocio"])}</span><p>{e(i["titulo"])}</p></div>'


def bloco_secoes(i):
    secoes = ""
    for sec in i.get("secoes", []):
        corpo = f'<p>{e(sec["texto"])}</p>' if sec.get("texto") else ""
        if sec.get("itens"):
            corpo += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in sec["itens"]) + "</ul>"
        if sec.get("texto_fim"):
            corpo += f'<p>{e(sec["texto_fim"])}</p>'
        secoes += f'<div class="im-sec"><h2>{e(sec["titulo"])}</h2>{corpo}</div>'
    if secoes:
        secoes = f'<section class="im-detalhes"><div class="wrap"><div class="im-secs">{secoes}</div></div></section>'
    return secoes


def hreflang(i):
    pt, en, fr = DOMINIO + url_pt(i), DOMINIO + url_en(i), DOMINIO + url_fr(i)
    return (f'<link rel="alternate" hreflang="pt" href="{pt}">\n'
            f'<link rel="alternate" hreflang="en" href="{en}">\n'
            f'<link rel="alternate" hreflang="fr" href="{fr}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{en}">')


def dados_estruturados(i, url, foto):
    return {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": i["titulo"],
        "description": i["descricao"],
        "url": url,
        "image": f"{DOMINIO}/imagens/{foto}",
        "offers": {"@type": "Offer", "priceCurrency": "EUR", "description": i["preco"], "businessFunction": i["negocio"]},
        "provider": {"@type": "RealEstateAgent", "name": "Liliana Pinto · Douro Lovers", "telephone": "+351934263986", "url": DOMINIO + "/"},
    }


def pagina(i, todos):
    url = f"{DOMINIO}/imoveis/{i['slug']}"
    foto = i.get("foto") or FOTO_PADRAO
    titulo = f"{i['titulo']} · {i['local']}"
    wa_txt = f"Olá Liliana, tenho interesse no imóvel {i['titulo']} ({i['local']})" + (f", {ref_txt(i)}" if i.get("ref") else "") + "."
    wa = f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(wa_txt)
    lista = "".join(f"<li>{e(c)}</li>" for c in i["caracteristicas"])
    imagem = bloco_imagem(i)
    secoes = bloco_secoes(i)
    outros = [o for o in todos if o["slug"] != i["slug"]][:3]
    outros_html = "\n".join(cartao(o, img="/imagens/") for o in outros)
    dados = dados_estruturados(i, url, foto)
    ref_linha = f'<span class="ref">{e(ref_txt(i))}</span>' if i.get("ref") else ""
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)} · Liliana Pinto</title>
<meta name="description" content="{e(i['descricao'])}">
<link rel="canonical" href="{url}">
{hreflang(i)}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(i['titulo'])} · {e(i['preco'])}">
<meta property="og:description" content="{e(i['local'])} · {e(' · '.join(i['caracteristicas']))}">
<meta property="og:image" content="{DOMINIO}/imagens/{e(foto)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>html,body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/estilo.css">
<script type="application/ld+json">{json.dumps(dados, ensure_ascii=False)}</script>
<script src="/analytics.js" defer></script>
</head>
<body>
<header><div class="wrap nav">
 <a class="brand" href="/"><span class="mono"><b>L</b><i>P</i></span><span>LILIANA PINTO</span></a>
 <nav aria-label="Secções"><a href="/#imoveis">Imóveis</a><a href="/#sobre">Sobre mim</a><a href="/en/">2FlagsHome</a><a href="/#contacto">Contacto</a></nav>
</div></header>
<main>
<div class="wrap"><p class="crumbs"><a href="/">Início</a> › <a href="/#imoveis">Imóveis</a> › {e(i['titulo'])}</p></div>
<div class="wrap im-hero">
 {imagem}
 <div class="im-info">
  <p class="loc">{e(i['local'])}</p>
  <h1>{e(i['titulo'])}</h1>
  <div class="pf"><span class="price">{e(i['preco'])}</span>{ref_linha}</div>
  <ul class="im-lista">{lista}</ul>
  <p>{e(i['descricao'])}</p>
  <div class="btns"><a class="btn solid" href="{e(wa)}" target="_blank" rel="noopener">Perguntar no WhatsApp</a><a class="btn ghost" href="#pedido">Marcar visita</a></div>
  <p class="im-dl"><a href="{e(i['douro_lovers'])}" target="_blank" rel="noopener">Ficha completa e todas as fotos na Douro Lovers →</a></p>
  <p class="im-lang">Não é bem este? <a href="/#procura">Diga-me o que procura e eu encontro.</a></p>
  <p class="im-lang"><a href="{url_en(i)}" hreflang="en" lang="en">Read this listing in English</a> · <a href="{url_fr(i)}" hreflang="fr" lang="fr">Lire cette annonce en français</a></p>
 </div>
</div>
{secoes}
<section id="pedido" class="im-pedido"><div class="wrap contact">
 <div><p class="eyebrow">Visitas e informações</p><h2>Quer ver <em>este imóvel?</em></h2><p class="lead" style="margin:0">Deixe o seu contacto e eu ligo-lhe para combinar a visita, presencial ou por videochamada. Respondo no próprio dia.</p></div>
 <form class="form" name="imovel" method="POST" action="/obrigado" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="subject" value="Pedido sobre imóvel · 2flagshome.com">
  <input type="hidden" name="imovel" value="{e(i['titulo'])} · {e(i['local'])} {e(ref_txt(i))}">
  <p class="hp"><label>Não preencher <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <label>Nome<input type="text" name="nome" autocomplete="name" required></label>
  <label>Telefone<input type="tel" name="telefone" autocomplete="tel"></label>
  <label class="full">Email<input type="email" name="email" autocomplete="email" required></label>
  <label class="full">Mensagem<textarea name="mensagem" placeholder="Quando lhe dá jeito visitar? Alguma pergunta sobre o imóvel?"></textarea></label>
  {campo_como_conheceu("pt", "como_conheceu")}
  <button class="btn solid full" type="submit">Pedir visita</button>
 </form>
</div></section>
<section class="im-outros"><div class="wrap">
 <div class="sec-head"><div><p class="eyebrow">Mais imóveis</p><h2>Também pode <em>gostar</em></h2></div><a class="btn ghost" href="/#imoveis">Ver todos</a></div>
 <div class="props props-3">
{outros_html}
 </div>
</div></section>
</main>
<a class="wa" href="{e(wa)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">WhatsApp</a>
<footer><div class="wrap foot"><div style="display:flex;align-items:center;gap:14px"><span class="mono"><b>L</b><i>P</i></span><span>LILIANA PINTO · CONSULTORA IMOBILIÁRIA</span></div><img src="/imagens/logo-douro-lovers.png" alt="Douro Lovers"><span>AMI 18696</span><a href="#" data-cookies style="color:inherit">Cookies</a></div></footer>
</body>
</html>
"""


def pagina_en(i, todos):
    pt = i
    i = em_ingles(i)
    url = DOMINIO + url_en(pt)
    foto = i.get("foto") or FOTO_PADRAO
    titulo = f"{i['titulo']} · {i['local']}"
    wa_txt = f"Hello Liliana, I'm interested in the home {i['titulo']} ({i['local']})" + (f", {ref_txt(i)}" if i.get("ref") else "") + "."
    wa = f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(wa_txt)
    lista = "".join(f"<li>{e(c)}</li>" for c in i["caracteristicas"])
    imagem = bloco_imagem(i)
    secoes = bloco_secoes(i)
    outros = [o for o in todos if o["slug"] != pt["slug"]][:3]
    outros_html = "\n".join(cartao_en(o) for o in outros)
    dados = dados_estruturados(i, url, foto)
    ref_linha = f'<span class="ref">{e(ref_txt(i))}</span>' if i.get("ref") else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)} · 2FlagsHome</title>
<meta name="description" content="{e(i['descricao'])}">
<link rel="canonical" href="{url}">
{hreflang(pt)}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(i['titulo'])} · {e(i['preco'])}">
<meta property="og:description" content="{e(i['local'])} · {e(' · '.join(i['caracteristicas']))}">
<meta property="og:image" content="{DOMINIO}/imagens/{e(foto)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>html,body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/estilo.css">
<script type="application/ld+json">{json.dumps(dados, ensure_ascii=False)}</script>
<script src="/analytics.js" defer></script>
</head>
<body>
<header><div class="wrap nav">
 <a class="brand" href="/en/"><span class="mono"><b>L</b><i>P</i></span><span>2FLAGSHOME</span></a>
 <nav aria-label="Sections"><a href="/en/#homes">Homes</a><a href="/en/guides/buying-a-home-in-portugal">Buying guide</a><a href="/en/#faq">FAQ</a><a href="/en/#contact">Contact</a></nav>
 <div class="langs" role="group" aria-label="Language"><a href="{url_pt(pt)}" hreflang="pt" lang="pt">PT</a><a href="{url_en(pt)}" hreflang="en" lang="en" aria-current="page">EN</a><a href="{url_fr(pt)}" hreflang="fr" lang="fr">FR</a></div>
</div></header>
<main>
<div class="wrap"><p class="crumbs"><a href="/en/">Home</a> › <a href="/en/#homes">Homes</a> › {e(i['titulo'])}</p></div>
<div class="wrap im-hero">
 {imagem}
 <div class="im-info">
  <p class="loc">{e(i['local'])}</p>
  <h1>{e(i['titulo'])}</h1>
  <div class="pf"><span class="price">{e(i['preco'])}</span>{ref_linha}</div>
  <ul class="im-lista">{lista}</ul>
  <p>{e(i['descricao'])}</p>
  <div class="btns"><a class="btn solid" href="{e(wa)}" target="_blank" rel="noopener">Ask on WhatsApp</a><a class="btn ghost" href="#enquiry">Book a viewing</a></div>
  <p class="im-dl"><a href="{e(i['douro_lovers'])}" target="_blank" rel="noopener">Full listing and all photos on Douro Lovers (in Portuguese) →</a></p>
  <p class="im-lang">Not quite right? <a href="/en/#contact">Tell me what you are looking for and I will find it.</a></p>
  <p class="im-lang">New to buying in Portugal? <a href="/en/guides/buying-a-home-in-portugal">Read the step-by-step guide.</a></p>
 </div>
</div>
{secoes}
<section id="enquiry" class="im-pedido"><div class="wrap contact">
 <div><p class="eyebrow">Viewings and information</p><h2>Would you like to <em>see this home?</em></h2><p class="lead" style="margin:0">Leave your details and I will get back to you to arrange a viewing, in person or by video call. I reply the same day, in English, French or Portuguese.</p></div>
 <form class="form" name="home-enquiry" method="POST" action="/obrigado" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="subject" value="Home enquiry (EN) · 2flagshome.com">
  <input type="hidden" name="home" value="{e(i['titulo'])} · {e(i['local'])} {e(ref_txt(i))}">
  <p class="hp"><label>Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <label>Name<input type="text" name="name" autocomplete="name" required></label>
  <label>Phone or WhatsApp<input type="tel" name="phone" autocomplete="tel"></label>
  <label>Email<input type="email" name="email" autocomplete="email" required></label>
  <label>Country you live in<input type="text" name="country" autocomplete="country-name"></label>
  <label class="full">Message<textarea name="message" placeholder="When would suit you for a viewing? Any questions about the home?"></textarea></label>
  {campo_como_conheceu("en", "how_found")}
  <button class="btn solid full" type="submit">Request a viewing</button>
 </form>
</div></section>
<section class="im-outros"><div class="wrap">
 <div class="sec-head"><div><p class="eyebrow">More homes</p><h2>You may <em>also like</em></h2></div><a class="btn ghost" href="/en/#homes">See all</a></div>
 <div class="props props-3">
{outros_html}
 </div>
</div></section>
</main>
<a class="wa" href="{e(wa)}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">WhatsApp</a>
<footer><div class="wrap foot"><div style="display:flex;align-items:center;gap:14px"><span class="mono"><b>L</b><i>P</i></span><span>2FLAGSHOME · LILIANA PINTO · LICENSED REAL ESTATE CONSULTANT</span></div><img src="/imagens/logo-douro-lovers.png" alt="Douro Lovers"><span>AMI 18696</span><a href="#" data-cookies style="color:inherit">Cookies</a></div></footer>
</body>
</html>
"""



def pagina_fr(i, todos):
    pt = i
    i = em_frances(i)
    url = DOMINIO + url_fr(pt)
    foto = i.get("foto") or FOTO_PADRAO
    titulo = f"{i['titulo']} · {i['local']}"
    wa_txt = f"Bonjour Liliana, je suis intéressé(e) par le bien {i['titulo']} ({i['local']})" + (f", {ref_txt(i)}" if i.get("ref") else "") + "."
    wa = f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(wa_txt)
    lista = "".join(f"<li>{e(c)}</li>" for c in i["caracteristicas"])
    imagem = bloco_imagem(i)
    secoes = bloco_secoes(i)
    outros = [o for o in todos if o["slug"] != pt["slug"]][:3]
    outros_html = "\n".join(cartao_fr(o) for o in outros)
    dados = dados_estruturados(i, url, foto)
    ref_linha = f'<span class="ref">{e(ref_txt(i))}</span>' if i.get("ref") else ""
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)} · 2FlagsHome</title>
<meta name="description" content="{e(i['descricao'])}">
<link rel="canonical" href="{url}">
{hreflang(pt)}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(i['titulo'])} · {e(i['preco'])}">
<meta property="og:description" content="{e(i['local'])} · {e(' · '.join(i['caracteristicas']))}">
<meta property="og:image" content="{DOMINIO}/imagens/{e(foto)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>html,body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/estilo.css">
<script type="application/ld+json">{json.dumps(dados, ensure_ascii=False)}</script>
<script src="/analytics.js" defer></script>
</head>
<body>
<header><div class="wrap nav">
 <a class="brand" href="/fr/"><span class="mono"><b>L</b><i>P</i></span><span>2FLAGSHOME</span></a>
 <nav aria-label="Sections"><a href="/fr/#homes">Biens</a><a href="/fr/guides/acheter-un-bien-au-portugal">Guide d'achat</a><a href="/fr/#faq">FAQ</a><a href="/fr/#contact">Contact</a></nav>
 <div class="langs" role="group" aria-label="Langue"><a href="{url_pt(pt)}" hreflang="pt" lang="pt">PT</a><a href="{url_en(pt)}" hreflang="en" lang="en">EN</a><a href="{url_fr(pt)}" hreflang="fr" lang="fr" aria-current="page">FR</a></div>
</div></header>
<main>
<div class="wrap"><p class="crumbs"><a href="/fr/">Accueil</a> › <a href="/fr/#homes">Biens</a> › {e(i['titulo'])}</p></div>
<div class="wrap im-hero">
 {imagem}
 <div class="im-info">
  <p class="loc">{e(i['local'])}</p>
  <h1>{e(i['titulo'])}</h1>
  <div class="pf"><span class="price">{e(i['preco'])}</span>{ref_linha}</div>
  <ul class="im-lista">{lista}</ul>
  <p>{e(i['descricao'])}</p>
  <div class="btns"><a class="btn solid" href="{e(wa)}" target="_blank" rel="noopener">Demander sur WhatsApp</a><a class="btn ghost" href="#enquiry">Réserver une visite</a></div>
  <p class="im-dl"><a href="{e(i['douro_lovers'])}" target="_blank" rel="noopener">Annonce complète et toutes les photos sur Douro Lovers (en portugais) →</a></p>
  <p class="im-lang">Ce n'est pas tout à fait ça ? <a href="/fr/#contact">Dites-moi ce que vous cherchez, je le trouve pour vous.</a></p>
  <p class="im-lang">Première acquisition au Portugal ? <a href="/fr/guides/acheter-un-bien-au-portugal">Lisez le guide étape par étape.</a></p>
 </div>
</div>
{secoes}
<section id="enquiry" class="im-pedido"><div class="wrap contact">
 <div><p class="eyebrow">Visites et informations</p><h2>Vous souhaitez <em>visiter ce bien ?</em></h2><p class="lead" style="margin:0">Laissez vos coordonnées et je vous recontacte pour organiser une visite, sur place ou par appel vidéo. Je réponds le jour même, en français, en anglais ou en portugais.</p></div>
 <form class="form" name="demande-bien" method="POST" action="/obrigado" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="subject" value="Demande de bien (FR) · 2flagshome.com">
  <input type="hidden" name="bien" value="{e(i['titulo'])} · {e(i['local'])} {e(ref_txt(i))}">
  <p class="hp"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <label>Nom<input type="text" name="nom" autocomplete="name" required></label>
  <label>Téléphone ou WhatsApp<input type="tel" name="telephone" autocomplete="tel"></label>
  <label>Email<input type="email" name="email" autocomplete="email" required></label>
  <label>Pays de résidence<input type="text" name="pays" autocomplete="country-name"></label>
  <label class="full">Message<textarea name="message" placeholder="Quand souhaitez-vous visiter ? Des questions sur le bien ?"></textarea></label>
  {campo_como_conheceu("fr", "how_found")}
  <button class="btn solid full" type="submit">Demander une visite</button>
 </form>
</div></section>
<section class="im-outros"><div class="wrap">
 <div class="sec-head"><div><p class="eyebrow">Autres biens</p><h2>Ils pourraient <em>aussi vous plaire</em></h2></div><a class="btn ghost" href="/fr/#homes">Tout voir</a></div>
 <div class="props props-3">
{outros_html}
 </div>
</div></section>
</main>
<a class="wa" href="{e(wa)}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp">WhatsApp</a>
<footer><div class="wrap foot"><div style="display:flex;align-items:center;gap:14px"><span class="mono"><b>L</b><i>P</i></span><span>2FLAGSHOME · LILIANA PINTO · CONSEILLÈRE IMMOBILIÈRE</span></div><img src="/imagens/logo-douro-lovers.png" alt="Douro Lovers"><span>AMI 18696</span><a href="#" data-cookies style="color:inherit">Cookies</a></div></footer>
</body>
</html>
"""

def substituir(ficheiro, marca, conteudo):
    h = ficheiro.read_text(encoding="utf-8")
    h, n = re.subn(rf"(<!-- {marca}:INICIO -->\n).*?(<!-- {marca}:FIM -->)", lambda m: m.group(1) + conteudo + "\n" + m.group(2), h, flags=re.S)
    assert n == 1, f"marcadores {marca} não encontrados em {ficheiro.name}"
    ficheiro.write_text(h, encoding="utf-8")


def sitemap(imoveis):
    hoje = datetime.date.today().isoformat()
    casa = {"pt": "/", "en": "/en/", "fr": "/fr/"}
    grupos = [casa] + [{"pt": url_pt(i), "en": url_en(i), "fr": url_fr(i)} for i in imoveis] + GUIAS + SERVICOS
    entradas = []
    for g in grupos:
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{DOMINIO}{u}"/>' for l, u in g.items())
        for u in g.values():
            entradas.append(f"  <url><loc>{DOMINIO}{u}</loc><lastmod>{hoje}</lastmod>{alt}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(entradas) + "\n</urlset>\n")


def main():
    imoveis = json.loads((RAIZ / "dados" / "imoveis.json").read_text(encoding="utf-8"))
    for lingua in ("en", "fr"):
        falta = [i["slug"] for i in imoveis if lingua not in i]
        assert not falta, f"falta a versão \"{lingua}\" em: {', '.join(falta)}"
    for pasta in (SITE / "imoveis", SITE / "en" / "homes", SITE / "fr" / "biens"):
        pasta.mkdir(exist_ok=True)
        for velho in pasta.glob("*.html"):
            velho.unlink()
    for i in imoveis:
        (SITE / "imoveis" / f"{i['slug']}.html").write_text(pagina(i, imoveis), encoding="utf-8")
        (SITE / "en" / "homes" / f"{i['en']['slug']}.html").write_text(pagina_en(i, imoveis), encoding="utf-8")
        (SITE / "fr" / "biens" / f"{i['fr']['slug']}.html").write_text(pagina_fr(i, imoveis), encoding="utf-8")

    substituir(SITE / "index.html", "IMOVEIS", "\n".join(cartao(i) for i in imoveis))
    substituir(SITE / "en" / "index.html", "HOMES", "\n".join(cartao_en(i) for i in imoveis))
    substituir(SITE / "fr" / "index.html", "HOMES", "\n".join(cartao_fr(i) for i in imoveis))
    (SITE / "sitemap.xml").write_text(sitemap(imoveis), encoding="utf-8")
    print(f"{len(imoveis)} imóveis gerados (PT, EN e FR)")

if __name__ == "__main__":
    main()
