# Resumo do Artigo M-AxPPA

Este documento resume, em linguagem de portfolio, os pontos publicos do artigo sobre **M-AxPPA: Modified Approximate Parallel Prefix Adder**.

## Contexto

Computacao aproximada busca reduzir custo de hardware, consumo de energia e area aceitando pequenas perdas de precisao. Essa abordagem e util em aplicacoes tolerantes a erro, como processamento de imagem, video, sinais e alguns cenarios de aprendizado de maquina.

Somadores sao blocos fundamentais em arquiteturas digitais. O artigo propoe uma modificacao em somadores paralelos prefixados aproximados, combinando AxPPA com tecnicas conhecidas da literatura.

## Proposta

A familia proposta e chamada de **M-AxPPA**.

Ela combina tres regioes:

- `M`: parte exata, usando bits mais significativos;
- `L`: parte intermediaria com AxPPA;
- `K`: parte menos significativa aproximada, usando uma tecnica simples da literatura.

As variantes principais sao:

- `M-AxPPA-COPY`
- `M-AxPPA-TRUNC`
- `M-AxPPA-LOA`

Para `W = 16`, o artigo explora 105 configuracoes `(M, L, K)` por variante, totalizando 315 arquiteturas M-AxPPA.

## Metricas

O artigo avalia qualidade e erro com:

- `SSIM`: similaridade estrutural;
- `NCC`: correlacao cruzada normalizada;
- `MAE`: erro absoluto medio;
- `MRE`: erro relativo medio;
- `MRED`: distancia media relativa de erro.

Tambem compara os resultados com metricas de sintese logica:

- economia de energia;
- economia de area;
- potencia;
- area.

## Comparacao Com A Literatura

O artigo compara M-AxPPA com arquiteturas aproximadas conhecidas:

- `COPY`
- `LOA`
- `TRUNC`
- `LDCA`
- `LZTA`
- `M-HEAA`
- `AxPPA`
- `HOERAA`

## Resultados Publicos Relevantes

O framework proposto avalia as 315 arquiteturas em cerca de 136,97 segundos e reduz a necessidade de sintese logica em 95,52%.

Entre as variantes M-AxPPA:

- `M-AxPPA-LOA` tende a ter melhor acuracia;
- `M-AxPPA-TRUNC` tende a economizar mais area e energia, aceitando erro maior;
- configuracoes intermediarias podem oferecer bons trade-offs.

## Como Este Projeto Usa O Artigo

Este portfolio transforma o artigo em um problema de dados:

> Dado um conjunto de arquiteturas aproximadas e suas metricas, como escolher a melhor configuracao para diferentes restricoes de erro, energia e area?

No primeiro MVP, usamos dados sinteticos baseados na estrutura e no comportamento qualitativo descrito no artigo.

