# Estudo de Caso V1 - Analise de Trade-offs em Computacao Aproximada

## Contexto

Computacao aproximada e uma estrategia usada para reduzir consumo de energia, area de hardware e custo computacional aceitando pequenos erros controlados. Essa abordagem e especialmente relevante em aplicacoes tolerantes a erro, como processamento de imagens, videos, sinais e alguns cenarios de inteligencia artificial.

Este projeto foi inspirado em um artigo publico sobre **M-AxPPA: Modified Approximate Parallel Prefix Adder**, apresentado em contexto academico. A proposta do portfolio nao e reivindicar autoria sobre a arquitetura original, mas transformar o problema tecnico em um estudo de dados.

## Problema De Dados

A pergunta central do projeto e:

> Dado um conjunto de arquiteturas aproximadas, quais configuracoes oferecem o melhor equilibrio entre erro, economia de energia e economia de area?

Essa pergunta e um problema classico de decisao com multiplos objetivos. Uma arquitetura pode economizar muita energia, mas gerar erro alto. Outra pode ter erro baixo, mas economia menor.

## Dados

Como os dados experimentais completos ainda nao estao disponiveis para divulgacao, a V1 usa dados sinteticos baseados na estrutura publica do artigo.

O dataset contem:

- 315 arquiteturas M-AxPPA;
- 128 arquiteturas baseline da literatura;
- 443 arquiteturas no total;
- metricas de erro e qualidade, como `SSIM`, `NCC`, `MAE`, `MRE` e `MRED`;
- metricas de sintese, como economia de energia e economia de area.

Os dados sinteticos foram usados para demonstrar o fluxo analitico, nao para afirmar resultados reais de hardware.

## Metodo

O projeto foi dividido em seis etapas:

1. Geracao e organizacao dos dados.
2. Modelagem em banco SQLite.
3. Consultas SQL para responder perguntas de ranking e restricao.
4. Preparacao de dataset para dashboard em Power BI.
5. Construcao de dashboard no Power BI para comparar erro, energia e area.
6. Publicacao de dashboard interativo em Streamlit para exploracao online.

A principal logica de analise foi:

```text
Primeiro filtrar arquiteturas com erro aceitavel.
Depois ranquear por energia, area ou score balanceado.
```

Tambem foram marcadas candidatas de Pareto para destacar arquiteturas que nao
sao dominadas nas relacoes erro-energia e erro-area.

## Entregaveis Da V1

A primeira versao publica do projeto inclui:

- dataset sintetico estruturado para analise;
- banco SQLite com schema relacional;
- consultas SQL para rankings, filtros de erro e candidatas de Pareto;
- dataset Excel/CSV preparado para Power BI;
- dashboard no Power BI com comparacoes de energia, area, erro e variantes;
- print do dashboard no README;
- dashboard interativo publicado em Streamlit;
- documentacao de perguntas analiticas para aproximar o projeto de um caso de BI.

## Resultados Iniciais

No dataset sintetico, quando filtramos arquiteturas com `MRED <= 0.10`, aparecem candidatas com alta economia de energia e erro controlado.

Exemplo de candidata forte para energia:

```text
M-AxPPA-LOA, M=1, L=1, K=14
MRED: 0.0828
Economia de energia: 91.44%
Economia de area: 59.26%
```

Exemplo de candidata equilibrada:

```text
M-AxPPA-LOA, M=2, L=1, K=13
MRED: 0.0710
Economia de energia: 88.62%
Economia de area: 60.93%
```

Ao mudar o objetivo de energia para area, o ranking muda. Isso mostra que a melhor arquitetura depende da pergunta de negocio ou engenharia.

A analise de Pareto reforca esse ponto: algumas arquiteturas sao relevantes
porque entregam maior economia com erro controlado, enquanto outras sao
preferiveis quando a prioridade e reduzir area. A decisao final depende do
criterio escolhido para a aplicacao.

## Aprendizados De Dados

Este projeto demonstra:

- modelagem de dados experimentais;
- consultas SQL com `JOIN`, `WHERE`, `ORDER BY` e filtros;
- analise de trade-off entre metricas conflitantes;
- analise multiobjetivo com candidatas de Pareto;
- preparacao de dataset para BI;
- dashboard em Power BI;
- dashboard interativo em Streamlit;
- storytelling tecnico para tomada de decisao.

## Limitacoes

Os resultados da V1 usam dados sinteticos. Eles sao uteis para demonstrar analise, mas nao devem ser interpretados como medicoes reais.

Uma versao futura pode substituir ou complementar esses dados com resultados experimentais reais, caso eles possam ser divulgados.

## Proximos Passos

- Criar notebooks em Python para analise exploratoria.
- Melhorar a documentacao da versao publicada em Streamlit.
- Evoluir o dashboard Power BI com uma segunda pagina para ranking.
- Traduzir o estudo de caso para ingles.
