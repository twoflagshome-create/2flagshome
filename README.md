# 2flagshome.com

Site da Liliana Pinto (consultora imobiliária, Douro Lovers) e da 2FlagsHome.

- Os ficheiros do site estão na pasta `site/`. É isso que o Netlify publica (ver `netlify.toml`).
- Cada alteração guardada neste repositório é publicada automaticamente pelo Netlify em 2flagshome.com.

## Formulário de contacto

O formulário "contacto" usa o Netlify Forms. Os pedidos aparecem em Netlify, no separador **Forms** do projeto `lilianapinto`. Depois de enviar, a pessoa vê a página `obrigado.html`.

## Páginas

- `/` página principal (português)
- `/en/` e `/fr/` página 2FlagsHome completa, em inglês e francês
- `/imoveis/<nome>` uma página por imóvel, geradas automaticamente

## Acrescentar ou tirar um imóvel

1. Ponha a foto em `site/imagens/` (nome sem espaços nem acentos, por exemplo `imovel-t3-gaia.jpg`).
2. Acrescente (ou apague) a entrada do imóvel em `dados/imoveis.json`.
3. Corra `python3 ferramentas/gerar.py`. Isto cria as páginas dos imóveis, os cartões da página principal e o `sitemap.xml`.
4. Guarde no GitHub. O Netlify publica sozinho.

Projeto Netlify: https://app.netlify.com/projects/lilianapinto
