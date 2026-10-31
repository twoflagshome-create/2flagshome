"""Gera as páginas de serviços em português (site/servicos/).

O texto está aqui: mude-o e volte a correr  python3 ferramentas/servicos.py
"""
import html, json, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
D = "https://2flagshome.com"
WA = "https://wa.me/351934263986?text="

NAV = [("/servicos/", "Serviços para a casa"), ("/servicos/melhorias-para-vender", "Preparar para vender")]


def formulario(assunto):
    opcoes = ["Pintura e pequenas reparações", "Eletricista ou canalizador", "Certificado energético", "Limpeza ou mudanças", "Preparar a casa para vender", "Outro assunto"]
    ops = "".join(f"<option{' selected' if o == assunto else ''}>{o}</option>" for o in opcoes)
    return f'''<section class="im-pedido" id="orcamento"><div class="wrap contact">
 <div><p class="eyebrow">Pedido de contacto</p><h2>Conte-me o que <em>precisa</em></h2><p class="lead" style="margin:0">Descreva o trabalho e, se puder, junte uma fotografia. Respondo no próprio dia e ponho-o em contacto com quem o pode resolver.</p>
  <p style="margin-top:18px"><a class="btn ghost" href="{WA}Ol%C3%A1%20Liliana%2C%20preciso%20de%20um%20contacto%20para%20a%20minha%20casa." target="_blank" rel="noopener">Pedir por WhatsApp</a></p></div>
 <form class="form" name="servicos" method="POST" action="/obrigado" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="subject" value="Novo pedido de contacto para serviços · 2flagshome.com">
  <p class="hp"><label>Não preencher <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <label>Nome<input type="text" name="nome" autocomplete="name" required></label>
  <label>Telefone<input type="tel" name="telefone" autocomplete="tel" required></label>
  <label class="full">Email<input type="email" name="email" autocomplete="email"></label>
  <label>Do que precisa<select name="servico">{ops}</select></label>
  <label>Localidade do imóvel<input type="text" name="localidade" placeholder="ex.: Gaia, Matosinhos"></label>
  <label class="full">Já foi meu cliente?<select name="cliente"><option>Não, é a primeira vez</option><option>Sim, comprei ou vendi casa consigo</option><option>Sim, arrendei casa consigo</option></select></label>
  <label class="full">Descreva o trabalho<textarea name="mensagem" required placeholder="ex.: trocar 6 tomadas e 2 interruptores, torneira da cozinha a pingar…"></textarea></label>
  <label class="full">Fotografias (opcional)<input type="file" name="fotografia" accept="image/*"></label>
  <button class="btn solid full" type="submit">Pedir contacto</button>
  <p class="note full">O pedido é gratuito e sem compromisso. Os trabalhos são combinados e faturados diretamente pelo profissional.</p>
 </form>
</div></section>'''


def pagina(url, titulo, descricao, h1, conteudo, assunto, migalha, wa_txt, faq=()):
    canon = D + url
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": migalha, "serviceType": migalha,
           "description": descricao, "url": canon, "inLanguage": "pt",
           "areaServed": ["Vila Nova de Gaia", "Porto", "Matosinhos"],
           "provider": {"@type": "RealEstateAgent", "name": "Liliana Pinto · Consultora Imobiliária", "url": D + "/", "telephone": "+351934263986"}}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq]})
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == url else ""}>{t}</a>' for u, t in NAV)
    faq_html = ""
    if faq:
        faq_html = '\n <h2 id="perguntas">Perguntas frequentes</h2>\n <div class="faq">\n' + "".join(
            f"  <details><summary>{html.escape(p)}</summary><p>{html.escape(r)}</p></details>\n" for p, r in faq) + " </div>\n"
    crumbs = '<a href="/">Início</a> › ' + ("Serviços" if url == "/servicos/" else f'<a href="/servicos/">Serviços</a> › {migalha}')
    return f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{html.escape(descricao)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:image" content="{D}/imagens/liliana-retrato.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>html,body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/estilo.css">
{lds}<script src="/analytics.js" defer></script>
</head>
<body>
<header><div class="wrap nav">
 <a class="brand" href="/"><span class="mono"><b>L</b><i>P</i></span><span>LILIANA PINTO</span></a>
 <nav aria-label="Serviços">{nav}<a href="/#contacto">Contacto</a></nav>
</div></header>
<main>
<div class="wrap"><p class="crumbs">{crumbs}</p></div>
<article class="guia"><div class="wrap">
 <p class="eyebrow">Serviços · Gaia, Porto e Matosinhos</p>
 <h1>{h1}</h1>
{conteudo}{faq_html}</div></article>

{formulario(assunto)}
</main>
<a class="wa" href="{WA}{wa_txt}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">WhatsApp</a>
<footer><div class="wrap foot"><div style="display:flex;align-items:center;gap:14px"><span class="mono"><b>L</b><i>P</i></span><span>LILIANA PINTO · CONSULTORA IMOBILIÁRIA</span></div><img src="/imagens/logo-douro-lovers.png" alt="Douro Lovers"><span>AMI 18696</span><a href="#" data-cookies style="color:inherit">Cookies</a></div></footer>
</body>
</html>
'''


def caixa(titulo, linhas, id_=""):
    rows = "".join(f'   <div class="row"><div><div class="lbl">{a}</div><p class="cost-d">{b}</p></div></div>\n' for a, b in linhas)
    return f' <section{f" id=\"{id_}\"" if id_ else ""} class="guia-caixa">\n  <h2>{titulo}</h2>\n  <div class="rows">\n{rows}  </div>\n </section>\n'


# ---------- Página geral ----------
geral = ''' <p class="lead">Além de comprar, vender e arrendar, ajudo-o com o que a casa precisa à volta disso. Precisa de um pintor, de um eletricista ou do certificado energético? Diga-me o que é e eu ponho-o em contacto com profissionais da zona em quem confio.</p>
 <p class="guia-autor">Liliana Pinto, consultora imobiliária (Douro Lovers, AMI 18696). Para quem já foi meu cliente e para quem mora em Gaia, Porto ou Matosinhos.</p>
'''
geral += caixa("Com que posso ajudar", [
    ("Pintura e pequenas reparações", "Pintar uma divisão ou a casa toda, tapar fissuras, tratar humidades, afinar portas e estores."),
    ("Eletricista e canalizador", "Tomadas e interruptores, iluminação, torneiras, autoclismos, silicones e pequenas avarias."),
    ("Certificado energético", "Obrigatório para vender ou arrendar. Indico um perito qualificado e acompanho o processo."),
    ("Limpeza e mudanças", "Limpeza profunda antes de vender ou de entrar na casa nova, esvaziar e transportar móveis."),
    ("Preparar a casa para vender", "Digo-lhe que pequenos trabalhos compensam e quem os pode fazer. <a href=\"/servicos/melhorias-para-vender\">Ver a lista →</a>"),
])
geral += ''' <h2>Como funciona</h2>
 <ol class="guia-lista">
  <li><strong>Pedido</strong>: diga-me o que precisa, de preferência com uma fotografia.</li>
  <li><strong>Contacto</strong>: indico-lhe um profissional de confiança e passo-lhe o seu pedido.</li>
  <li><strong>Trabalho</strong>: combina o preço e a data diretamente com o profissional, que lhe passa a fatura.</li>
 </ol>
 <p>O contacto não tem custo para si. Se for meu cliente numa compra, venda ou arrendamento, acompanho também o trabalho.</p>
'''

# ---------- Melhorias para vender ----------
melhorias = ''' <p class="lead">Uma casa que parece bem cuidada vende-se mais depressa e negocia-se melhor. Não é preciso remodelar: na maior parte dos casos bastam pequenos trabalhos, feitos antes das fotografias, para o comprador deixar de ver defeitos e passar a imaginar-se lá a viver.</p>
 <p class="guia-autor">Quando avalio uma casa para venda, faço consigo esta lista, digo-lhe quais os trabalhos que compensam e ponho-o em contacto com quem os faz.</p>

 <nav class="guia-indice" aria-label="Nesta página"><p class="lbl">Nesta página</p><ol>
  <li><a href="#pintura">Pintura e paredes</a></li><li><a href="#eletricidade">Eletricidade e iluminação</a></li><li><a href="#banho">Casas de banho e canalização</a></li><li><a href="#cozinha">Cozinha</a></li><li><a href="#portas">Portas, janelas e estores</a></li><li><a href="#chao">Pavimentos e rodapés</a></li><li><a href="#exterior">Entrada, varandas e exterior</a></li><li><a href="#preparacao">Limpeza e apresentação</a></li><li><a href="#nao">O que não compensa</a></li>
 </ol></nav>
'''
melhorias += caixa("Pintura e paredes", [
    ("Pintar paredes e tetos", "Em branco ou cores neutras e claras. É o trabalho com mais impacto pelo valor que custa."),
    ("Tapar furos e fissuras", "Buracos de quadros, buchas antigas e pequenas fissuras, antes de pintar."),
    ("Tratar manchas de humidade e bolor", "Sobretudo em tetos de casas de banho e cantos de quartos. O comprador repara sempre nisto."),
    ("Retirar papel de parede ou cores fortes", "Uma divisão neutra parece maior e mais fácil de mobilar."),
], "pintura")
melhorias += caixa("Eletricidade e iluminação", [
    ("Trocar tomadas e interruptores", "Os amarelados, partidos ou de modelos diferentes. Espelhos novos e iguais em toda a casa."),
    ("Substituir lâmpadas e candeeiros", "Lâmpadas fundidas, casquilhos à vista e luz de cores diferentes. Luz branca quente e uniforme."),
    ("Verificar campainha, intercomunicador e quadro", "Pequenas avarias que dão má impressão logo à entrada."),
], "eletricidade")
melhorias += caixa("Casas de banho e canalização", [
    ("Refazer silicones e juntas", "Na base de duche, banheira e lavatório. Silicone escuro passa por falta de limpeza ou por infiltração."),
    ("Reparar torneiras e autoclismos", "Fugas e pingos, autoclismo que não para, sifões a verter."),
    ("Trocar tampo de sanita, chuveiro e acessórios", "Barato e faz a casa de banho parecer mais nova."),
    ("Desentupir e eliminar maus cheiros", "Ralos e esgotos lentos."),
], "banho")
melhorias += caixa("Cozinha", [
    ("Trocar puxadores e afinar portas e gavetas", "Portas desalinhadas e gavetas presas notam-se em todas as visitas."),
    ("Pintar ou forrar frentes de armários", "Alternativa económica a mudar a cozinha."),
    ("Rejuntar azulejos e substituir torneira", "Juntas limpas e uma torneira nova mudam o aspeto da bancada."),
], "cozinha")
melhorias += caixa("Portas, janelas e estores", [
    ("Afinar portas e trocar puxadores e fechaduras", "Portas que roçam, batem ou não fecham bem."),
    ("Reparar estores", "Fitas, molas e lâminas partidas. Um estore que não sobe numa visita é uma má surpresa."),
    ("Vedantes de janelas e portas exteriores", "Reduz correntes de ar e condensação."),
], "portas")
melhorias += caixa("Pavimentos e rodapés", [
    ("Reparar ou afagar soalho", "Riscos e zonas gastas. Um soalho recuperado é um ponto forte nos anúncios."),
    ("Substituir rodapés danificados", "Rodapés lascados ou soltos."),
    ("Limpar ou refazer juntas de mosaico", "Especialmente em cozinhas e casas de banho."),
], "chao")
melhorias += caixa("Entrada, varandas e exterior", [
    ("Pintar porta de entrada, portão e gradeamentos", "A primeira imagem que o comprador tem da casa."),
    ("Limpar varandas, terraços e caleiras", "Lavagem de pavimentos e retirada de entulho e vasos velhos."),
    ("Arranjar o jardim", "Corte de relva, poda e limpeza."),
    ("Número da porta, caixa de correio e iluminação exterior", "Pormenores pequenos que mostram cuidado."),
], "exterior")
melhorias += caixa("Limpeza e apresentação", [
    ("Limpeza profunda antes das fotografias", "Incluindo vidros, cozinha, casas de banho e varandas."),
    ("Esvaziar e arrumar", "Retirar móveis a mais e objetos pessoais antes das fotografias."),
    ("Home staging simples", "Têxteis, plantas e pequenos objetos para dar vida às divisões vazias."),
], "preparacao")
melhorias += ''' <h2 id="nao">O que normalmente não compensa</h2>
 <p>Antes de vender, raramente se recupera o dinheiro de uma remodelação grande, como uma cozinha ou casa de banho novas, mudar o pavimento de toda a casa ou abrir paredes. O comprador prefere escolher ele próprio esses acabamentos e conta com isso no preço. Nestes casos, o melhor é mostrar o potencial: um orçamento indicativo da obra, feito por um profissional, ajuda os interessados a decidir.</p>
'''

paginas = [
    ("index.html", "/servicos/", "Serviços para a casa em Gaia, Porto e Matosinhos · Liliana Pinto",
     "Precisa de um pintor, eletricista, canalizador ou do certificado energético? Ponho-o em contacto com profissionais de confiança em Gaia, Porto e Matosinhos.",
     "Serviços para a <em>sua casa</em>", geral, "Outro assunto", "Serviços para a casa", "Ol%C3%A1%20Liliana%2C%20gostava%20de%20saber%20mais%20sobre%20os%20servi%C3%A7os.", ()),
    ("melhorias-para-vender.html", "/servicos/melhorias-para-vender", "Pequenas obras para vender a casa a melhor preço · Liliana Pinto",
     "Lista de pequenas obras e melhorias que ajudam a vender a casa mais depressa e a melhor preço: pintura, eletricidade, casas de banho, cozinha e apresentação.",
     "Pequenas obras para <em>vender a casa a melhor preço</em>", melhorias, "Preparar a casa para vender", "Preparar para vender",
     "Ol%C3%A1%20Liliana%2C%20quero%20preparar%20a%20minha%20casa%20para%20vender.", ()),
]
pasta = SITE / "servicos"
pasta.mkdir(exist_ok=True)
for f, url, t, d, h1, c, a, m, w, q in paginas:
    (pasta / f).write_text(pagina(url, t, d, h1, c, a, m, w, q), encoding="utf-8")
print("ok", len(paginas))
