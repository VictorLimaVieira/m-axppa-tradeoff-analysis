# Primeiras Descobertas

Este relatorio usa o dataset sintetico inicial. Os resultados abaixo servem para validar o fluxo de analise, nao para afirmar medicoes reais de hardware.

## Validacao Do Dataset

O gerador criou:

- 315 arquiteturas `M-AxPPA`;
- 128 arquiteturas de baseline da literatura;
- 443 arquiteturas no total;
- 443 linhas em cada tabela principal de metricas;
- um banco SQLite em `database/m_axppa_synthetic.sqlite`.

## Primeiras Leituras

No dataset sintetico, arquiteturas com `TRUNC` tendem a aparecer com maior economia de energia e area, mas tambem com maior erro.

Arquiteturas com `LOA` tendem a preservar melhor acuracia, especialmente quando o limite de erro e mais rigoroso.

Arquiteturas com `COPY` ficam em uma regiao intermediaria, o que e util para explicar trade-offs.

## Exemplo De Pergunta Respondida

Pergunta:

> Qual arquitetura economiza mais energia mantendo `MRED <= 0.10`?

No dataset sintetico atual, uma candidata forte e:

```text
M-AxPPA-LOA, M=1, L=1, K=14
MRED aproximado: 0.0828
Economia de energia aproximada: 91.44%
Economia de area aproximada: 59.26%
```

Outra candidata importante e:

```text
M-AxPPA-LOA, M=2, L=1, K=13
MRED aproximado: 0.0710
Economia de energia aproximada: 88.62%
Economia de area aproximada: 60.93%
```

## Interpretacao

Essas candidatas mostram a historia central do projeto:

> Quando definimos um limite maximo de erro, a melhor arquitetura nao e necessariamente a que economiza mais em termos absolutos, mas a que entrega maior economia dentro da restricao de qualidade.

## Proxima Analise

As proximas etapas sao:

- expandir o notebook de EDA com mais visualizacoes;
- aprofundar a comparacao entre `COPY`, `TRUNC` e `LOA`;
- analisar como `M`, `L` e `K` influenciam erro, energia e area;
- evoluir a visualizacao dos candidatos de Pareto;
- transformar os principais achados em uma segunda pagina do Power BI.
