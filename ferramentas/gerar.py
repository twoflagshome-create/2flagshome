"""Gera as páginas dos imóveis, os cartões da página inicial e o sitemap.

Uso (na pasta do repositório):  python3 ferramentas/gerar.py
Os dados estão em dados/imoveis.json e as fotos em site/imagens/.
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

e = html.escape


def ref_txt(i):
    return f"Ref. {i['ref']}" if i.get("ref") else ""


def cartao(i):
    url = f"/imoveis/{i['slug']}"
    spec = " · ".join(i["caracteristicas"])
    ref = f'<span class="ref">{e(ref_txt(i))}</span>' if i.get("ref") else ""
    if i.get("foto"):
        pos = f' style="object-position:{i["foto_posicao"]}"' if i.get("foto_posicao") else ""
        return (
            f'<article class="prop">\n'
            f' <a class="ph" href="{url}"><img src="imagens/{e(i["foto"])}" alt="{e(i["alt"])}" loading="lazy"{pos}><span class="badge">{e(i["negocio"])}</span></a>\n'
            f' <div class="pb"><p class="loc">{e(i["local"])}</p><h3><a href="{url}">{e(i["titulo"])}</a></h3><p class="spec">{e(spec)}</p>\n'
            f' <div class="pf"><span class="price">{e(i["preco"])}</span>{ref}</div>\n'
            f' <a class="more" href="{url}">Ver imóvel →</a></div></article>'
        )
    return (
        f'<article class="prop plain"><div class="pb"><span class="badge static">{e(i["negocio"])}</span>'
        f'<p class="loc">{e(i["local"])}</p><h3><a href="{url}">{e(i["titulo"])}</a></h3><p class="spec">{e(spec)}</p>'
        f'<div class="pf"><span class="price">{e(i["preco"])}</span>{ref}</div>'
        f'<a class="more" href="{url}">Ver imóvel →</a></div></article>'
    )


def pagina(i, todos):
    url = f"{DOMINIO}/imoveis/{i['slug']}"
    foto = i.get("foto") or FOTO_PADRAO
    titulo = f"{i['titulo']} · {i['local']}"
    resumo = f"{i['negocio']} · {i['preco']} · " + " · ".join(i["caracteristicas"])
    wa_txt = f"Olá Liliana, tenho interesse no imóvel {i['titulo']} ({i['local']})" + (f", {ref_txt(i)}" if i.get("ref") else "") + "."
    wa = f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(wa_txt)
    lista = "".join(f"<li>{e(c)}</li>" for c in i["caracteristicas"])
    if i.get("foto"):
        pos = f' style="object-position:{i["foto_posicao"]}"' if i.get("foto_posicao") else ""
        imagem = f'<figure class="im-foto"><img src="/imagens/{e(i["foto"])}" alt="{e(i["alt"])}"{pos}><span class="badge">{e(i["negocio"])}</span></figure>'
    else:
        imagem = f'<div class="im-foto im-sem-foto"><span class="badge">{e(i["negocio"])}</span><p>{e(i["titulo"])}</p></div>'
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
    outros = [o for o in todos if o["slug"] != i["slug"]][:3]
    outros_html = "\n".join(cartao(o).replace('src="imagens/', 'src="/imagens/') for o in outros)
    dados = {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": i["titulo"],
        "description": i["descricao"],
        "url": url,
        "image": f"{DOMINIO}/imagens/{foto}",
        "offers": {"@type": "Offer", "priceCurrency": "EUR", "description": i["preco"], "businessFunction": i["negocio"]},
        "provider": {"@type": "RealEstateAgent", "name": "Liliana Pinto · Douro Lovers", "telephone": "+351934263986", "url": DOMINIO + "/"},
    }
    ref_linha = f'<span class="ref">{e(ref_txt(i))}</span>' if i.get("ref") else ""
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)} · Liliana Pinto</title>
<meta name="description" content="{e(i['descricao'])}">
<link rel="canonical" href="{url}">
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
  <p class="im-lang">English or French? <a href="/en/#contact">I can help in your language.</a></p>
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
<footer><div class="wrap foot"><div style="display:flex;align-items:center;gap:14px"><span class="mono"><b>L</b><i>P</i></span><span>LILIANA PINTO · CONSULTORA IMOBILIÁRIA</span></div><img src="/imagens/logo-douro-lovers.png" alt="Douro Lovers"><span>AMI 18696</span></div></footer>
</body>
</html>
"""


def main():
    imoveis = json.loads((RAIZ / "dados" / "imoveis.json").read_text(encoding="utf-8"))
    (SITE / "imoveis").mkdir(exist_ok=True)
    for velho in (SITE / "imoveis").glob("*.html"):
        velho.unlink()
    for i in imoveis:
        (SITE / "imoveis" / f"{i['slug']}.html").write_text(pagina(i, imoveis), encoding="utf-8")

    idx = SITE / "index.html"
    h = idx.read_text(encoding="utf-8")
    cartoes = "\n".join(cartao(i) for i in imoveis)
    h, n = re.subn(r"(<!-- IMOVEIS:INICIO -->\n).*?(\n<!-- IMOVEIS:FIM -->)", lambda m: m.group(1) + cartoes + m.group(2), h, flags=re.S)
    assert n == 1, "marcadores IMOVEIS não encontrados no index.html"
    idx.write_text(h, encoding="utf-8")

    hoje = datetime.date.today().isoformat()
    urls = ["/", "/en/", "/fr/"] + [f"/imoveis/{i['slug']}" for i in imoveis]
    linhas = "\n".join(f"  <url><loc>{DOMINIO}{u}</loc><lastmod>{hoje}</lastmod></url>" for u in urls)
    (SITE / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n',
        encoding="utf-8",
    )
    print(f"{len(imoveis)} imóveis gerados")


if __name__ == "__main__":
    main()
