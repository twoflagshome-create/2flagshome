"""Gera as páginas de serviços em português (site/servicos/).

O texto está aqui: mude-o e volte a correr  python3 ferramentas/servicos.py
"""
import html, json, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
D = "https://2flagshome.com"
WA = "https://wa.me/351934263986?text="

NAV = [("/servicos/", "Serviços"), ("/servicos/melhorias-para-vender", "Vender melhor"),
       ("/servicos/pequenas-reparacoes", "Reparações"), ("/servicos/gestao-de-arrendamento", "Arrendamento")]


def formulario(assunto):
    opcoes = ["Preparar a casa para vender", "Pequenas reparações", "Gestão de arrendamento", "Outro assunto"]
    ops = "".join(f"<option{' selected' if o == assunto else ''}>{o}</option>" for o in opcoes)
    return f'''<section class="im-pedido" id="orcamento"><div class="wrap contact">
 <div><p class="eyebrow">Pedido de orçamento</p><h2>Conte-me o que <em>precisa</em></h2><p class="lead" style="margin:0">Descreva o trabalho e, se puder, junte uma ou duas fotografias. Respondo no próprio dia com os próximos passos e, sempre que possível, com uma estimativa.</p>
  <p style="margin-top:18px"><a class="btn ghost" href="{WA}Ol%C3%A1%20Liliana%2C%20gostava%20de%20pedir%20um%20or%C3%A7amento." target="_blank" rel="noopener">Pedir por WhatsApp</a></p></div>
 <form class="form" name="servicos" method="POST" action="/obrigado" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="subject" value="Novo pedido de serviço · 2flagshome.com">
  <p class="hp"><label>Não preencher <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <label>Nome<input type="text" name="nome" autocomplete="name" required></label>
  <label>Telefone<input type="tel" name="telefone" autocomplete="tel" required></label>
  <label class="full">Email<input type="email" name="email" autocomplete="email"></label>
  <label>Serviço<select name="servico">{ops}</select></label>
  <label>Localidade do imóvel<input type="text" name="localidade" placeholder="ex.: Gaia, Matosinhos"></label>
  <label class="full">Já foi meu cliente?<select name="cliente"><option>Não, é a primeira vez</option><option>Sim, comprei ou vendi casa consigo</option><option>Sim, arrendei casa consigo</option></select></label>
  <label class="full">O que precisa<textarea name="mensagem" required placeholder="ex.: trocar 6 tomadas e 2 interruptores, torneira da cozinha a pingar…"></textarea></label>
  <label class="full">Fotografias (opcional)<input type="file" name="fotografia" accept="image/*"></label>
  <button class="btn solid full" type="submit">Pedir orçamento</button>
  <p class="note full">O pedido não tem custo nem compromisso.</p>
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
geral = ''' <p class="lead">Além de comprar, vender e arrendar, agora também trato da casa em si: as pequenas obras que ajudam a vender melhor, as reparações do dia a dia e a gestão completa do arrendamento. Para quem já foi meu cliente e para quem mora na zona.</p>
 <p class="guia-autor">Liliana Pinto, consultora imobiliária (Douro Lovers, AMI 18696). Cresci nas obras do meu pai e sei olhar para uma casa por dentro.</p>

 <div class="services svc-links">
  <a class="svc" href="/servicos/melhorias-para-vender"><h3>Preparar para vender</h3><p>Pintura, reparações e pequenos acabamentos que fazem a casa parecer cuidada nas fotografias e nas visitas.</p><span class="more">Ver a lista →</span></a>
  <a class="svc" href="/servicos/pequenas-reparacoes"><h3>Pequenas reparações</h3><p>Tomadas, torneiras, portas, estores, silicones e pintura. Aqueles trabalhos que ninguém quer vir fazer.</p><span class="more">Ver serviços →</span></a>
  <a class="svc" href="/servicos/gestao-de-arrendamento"><h3>Gestão de arrendamento</h3><p>Do anúncio ao inquilino certo, contrato, rendas, avarias e vistorias. Ideal se vive longe ou no estrangeiro.</p><span class="more">Ver serviços →</span></a>
 </div>

 <h2>Para quem</h2>
 <ul>
  <li><strong>Clientes que compraram ou venderam casa comigo</strong>: continuo a ser o seu contacto depois da escritura, para arranjar o que for preciso.</li>
  <li><strong>Proprietários e famílias da zona</strong> de Gaia, Porto e Matosinhos que precisam de um trabalho bem feito, com orçamento claro.</li>
  <li><strong>Proprietários que vivem no estrangeiro</strong> e querem a casa em Portugal arrendada e acompanhada sem terem de vir cá.</li>
 </ul>

 <h2>Como funciona</h2>
 <ol class="guia-lista">
  <li><strong>Pedido</strong>: diga-me o que precisa, de preferência com fotografias.</li>
  <li><strong>Orçamento</strong>: envio um valor fechado antes de começar. Se for preciso, vou ver a casa.</li>
  <li><strong>Trabalho</strong>: marcamos o dia. Se não puder estar presente, eu abro a casa e acompanho.</li>
  <li><strong>Fecho</strong>: envio fotografias do trabalho feito e a fatura.</li>
 </ol>
'''

# ---------- Melhorias para vender ----------
melhorias = ''' <p class="lead">Uma casa que parece bem cuidada vende-se mais depressa e negocia-se melhor. Não é preciso remodelar: na maior parte dos casos bastam pequenos trabalhos, feitos antes das fotografias, para o comprador deixar de ver defeitos e passar a imaginar-se lá a viver.</p>
 <p class="guia-autor">Quando avalio uma casa para venda, faço consigo esta lista e digo-lhe quais os trabalhos que compensam e quais não valem a pena.</p>

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
    ("Esvaziar e arrumar", "Retirar móveis a mais e objetos pessoais. Levamos o que for para deitar fora."),
    ("Home staging simples", "Têxteis, plantas e pequenos objetos para dar vida às divisões vazias."),
], "preparacao")
melhorias += ''' <h2 id="nao">O que normalmente não compensa</h2>
 <p>Antes de vender, raramente se recupera o dinheiro de uma remodelação grande, como uma cozinha ou casa de banho novas, mudar o pavimento de toda a casa ou abrir paredes. O comprador prefere escolher ele próprio esses acabamentos e conta com isso no preço. Nestes casos, o melhor é mostrar o potencial: faço um orçamento indicativo da obra para entregar aos interessados.</p>
'''

# ---------- Pequenas reparações ----------
reparacoes = ''' <p class="lead">Aqueles trabalhos pequenos que se vão adiando porque ninguém quer vir fazer: uma tomada solta, uma torneira a pingar, um estore preso. Envie-me fotografias e eu trato do resto, com profissionais de confiança e orçamento fechado antes de começar.</p>
'''
reparacoes += caixa("Eletricidade", [
    ("Tomadas e interruptores", "Substituição, reparação e mudança de espelhos."),
    ("Candeeiros e iluminação", "Montagem de candeeiros, focos e iluminação LED."),
    ("Pequenas avarias", "Campainhas, intercomunicadores e disjuntores que disparam."),
])
reparacoes += caixa("Canalização", [
    ("Torneiras e misturadoras", "Reparação de fugas e substituição."),
    ("Autoclismos, sifões e ralos", "Fugas, entupimentos e maus cheiros."),
    ("Silicones e juntas", "Base de duche, banheira, lavatório e bancada."),
    ("Esquentadores e termoacumuladores", "Ver a avaria e tratar da substituição, com técnico certificado para o gás."),
])
reparacoes += caixa("Carpintaria, portas e estores", [
    ("Portas e fechaduras", "Afinação, puxadores, fechaduras e cilindros."),
    ("Estores", "Fitas, molas, lâminas e motores."),
    ("Móveis e montagens", "Afinação de armários, montagem de móveis, prateleiras, cortinados e quadros."),
])
reparacoes += caixa("Pintura e pequenas remodelações", [
    ("Pintura de divisões ou de toda a casa", "Paredes, tetos, portas e rodapés."),
    ("Humidades e bolor", "Tratamento das manchas e pintura com tinta própria."),
    ("Pequenas remodelações", "Troca de loiças sanitárias, móvel de casa de banho, azulejos soltos e pavimento flutuante."),
])
reparacoes += ''' <h2>Porquê pedir-me a mim</h2>
 <ul>
  <li><strong>Um só contacto</strong> para vários trabalhos: não precisa de procurar um eletricista, um canalizador e um pintor.</li>
  <li><strong>Orçamento fechado</strong> antes de começar e fotografias no fim.</li>
  <li><strong>Abro a casa por si</strong> se estiver a trabalhar, fora ou a viver no estrangeiro.</li>
 </ul>
'''
faq_rep = [
    ("Fazem trabalhos muito pequenos, como trocar uma tomada?", "Sim. Para trabalhos pequenos, o ideal é juntar vários numa só visita, para o valor da deslocação compensar."),
    ("Quanto custa?", "Depende do trabalho. Com fotografias consigo, muitas vezes, dar uma estimativa logo no próprio dia. Antes de começar envio sempre um valor fechado."),
    ("Preciso de estar em casa?", "Não. Se me deixar uma chave, eu abro a casa, acompanho o trabalho e envio-lhe fotografias."),
    ("Que zonas cobrem?", "Vila Nova de Gaia, Porto e Matosinhos. Para outras zonas, pergunte-me."),
]

# ---------- Gestão de arrendamento ----------
gestao = ''' <p class="lead">Tem uma casa para arrendar e não quer, ou não pode, tratar de tudo? Eu encontro o inquilino, faço o contrato e, se quiser, continuo a acompanhar a casa: rendas, avarias, vistorias e a saída do inquilino.</p>
 <p class="guia-autor">Especialmente pensado para proprietários que vivem longe ou no estrangeiro, e para clientes que compraram casa para investir.</p>

 <h2>Duas formas de trabalhar</h2>
  <div class="services dois">
  <div class="svc"><h3>Arrendar</h3><p>Encontro o inquilino certo e trato do contrato. A partir da entrega das chaves, a gestão fica consigo.</p></div>
  <div class="svc"><h3>Gestão completa</h3><p>Tudo o que está no plano Arrendar e, depois, o acompanhamento da casa e do inquilino durante todo o contrato.</p></div>
 </div>
'''
gestao += caixa("Arrendar · encontrar o inquilino", [
    ("Valor da renda", "Estudo do mercado da zona para definir uma renda certa."),
    ("Preparação da casa", "Lista do que convém arranjar antes, fotografias e vídeo profissionais."),
    ("Anúncio e visitas", "Divulgação nos portais e redes, triagem de contactos e visitas acompanhadas."),
    ("Seleção do inquilino", "Verificação de rendimentos, contrato de trabalho e referências. Fiador ou caução, conforme o caso."),
    ("Contrato", "Preparação do contrato e comunicação às Finanças."),
    ("Entrega das chaves", "Inventário com fotografias e leituras dos contadores."),
])
gestao += caixa("Gestão completa · durante o contrato", [
    ("Rendas", "Controlo mensal dos pagamentos e contacto com o inquilino em caso de atraso."),
    ("Recibos e atualização anual", "Apoio na emissão dos recibos de renda eletrónicos e na atualização anual da renda."),
    ("Avarias", "O inquilino fala comigo e eu trato da reparação com a nossa equipa, com o seu acordo prévio."),
    ("Vistorias", "Visita periódica à casa, com relatório e fotografias."),
    ("Condomínio, seguros e contas", "Acompanhamento de assembleias, seguros e mudanças de titular."),
    ("Saída do inquilino", "Vistoria final, comparação com o inventário, caução e preparação para o próximo contrato."),
])
faq_ges = [
    ("Vivo no estrangeiro. Consigo arrendar a minha casa em Portugal?", "Sim. Trato de tudo no local e falamos por videochamada ou WhatsApp. Precisa de NIF português e, para alguns passos, de uma procuração."),
    ("Que documentos preciso para arrendar?", "A caderneta predial, a certidão permanente, a licença de utilização e o certificado energético, que é obrigatório para anunciar. Se faltar algum, ajudo a tratar."),
    ("Quanto custa a gestão?", "Depende do plano e da casa. Peça-me uma proposta: envio os valores por escrito antes de qualquer compromisso."),
    ("Posso começar só com o plano Arrendar e passar depois para a gestão completa?", "Sim, a qualquer altura do contrato."),
]

paginas = [
    ("index.html", "/servicos/", "Serviços para a sua casa · Remodelações e gestão de arrendamento · Liliana Pinto",
     "Pequenas obras para vender melhor, pequenas reparações e gestão de arrendamento em Gaia, Porto e Matosinhos. Um só contacto, orçamento fechado.",
     "Serviços para a <em>sua casa</em>", geral, "Outro assunto", "Serviços", "Ol%C3%A1%20Liliana%2C%20gostava%20de%20saber%20mais%20sobre%20os%20servi%C3%A7os.", ()),
    ("melhorias-para-vender.html", "/servicos/melhorias-para-vender", "Pequenas obras para vender a casa a melhor preço · Liliana Pinto",
     "Lista de pequenas obras e melhorias que ajudam a vender a casa mais depressa e a melhor preço: pintura, eletricidade, casas de banho, cozinha e apresentação.",
     "Pequenas obras para <em>vender a casa a melhor preço</em>", melhorias, "Preparar a casa para vender", "Preparar para vender",
     "Ol%C3%A1%20Liliana%2C%20quero%20preparar%20a%20minha%20casa%20para%20vender.", ()),
    ("pequenas-reparacoes.html", "/servicos/pequenas-reparacoes", "Pequenas reparações em Gaia, Porto e Matosinhos · Liliana Pinto",
     "Troca de tomadas e interruptores, torneiras, autoclismos, estores, portas, silicones e pintura em Gaia, Porto e Matosinhos. Orçamento fechado.",
     "Pequenas reparações <em>em casa</em>", reparacoes, "Pequenas reparações", "Pequenas reparações",
     "Ol%C3%A1%20Liliana%2C%20preciso%20de%20uma%20pequena%20repara%C3%A7%C3%A3o.", faq_rep),
    ("gestao-de-arrendamento.html", "/servicos/gestao-de-arrendamento", "Gestão de arrendamento em Gaia, Porto e Matosinhos · Liliana Pinto",
     "Gestão de arrendamento para proprietários: seleção do inquilino, contrato, rendas, avarias e vistorias. Ideal para quem vive longe ou no estrangeiro.",
     "Gestão de <em>arrendamento</em>", gestao, "Gestão de arrendamento", "Gestão de arrendamento",
     "Ol%C3%A1%20Liliana%2C%20tenho%20uma%20casa%20para%20arrendar.", faq_ges),
]
pasta = SITE / "servicos"
pasta.mkdir(exist_ok=True)
for f, url, t, d, h1, c, a, m, w, q in paginas:
    (pasta / f).write_text(pagina(url, t, d, h1, c, a, m, w, q), encoding="utf-8")
print("ok", len(paginas))
