# 2flagshome.com

Site da Liliana Pinto (consultora imobiliária, Douro Lovers) e da 2FlagsHome.

- Os ficheiros do site estão na pasta `site/`. É isso que o Netlify publica (ver `netlify.toml`).
- Cada alteração guardada neste repositório é publicada automaticamente pelo Netlify em 2flagshome.com.

## Formulário de contacto

O formulário "contacto" usa o Netlify Forms. Os pedidos aparecem em Netlify, no separador **Forms** do projeto `lilianapinto`. Depois de enviar, a pessoa vê a página `obrigado.html`.

## Acrescentar um imóvel

1. Ponha a foto em `site/imagens/` (nome sem espaços nem acentos, por exemplo `imovel-t3-gaia.jpg`).
2. Em `site/index.html`, copie um bloco `<article class="prop"> ... </article>` e troque a foto, a etiqueta (Venda / Arrendamento / Trespasse), a zona, o título, as características, o preço, a referência e o link da Douro Lovers.
3. Para tirar um imóvel vendido, apague o bloco dele.
