# Metodologia dos Dados Sinteticos

## Por Que Usar Dados Sinteticos?

No momento, o projeto possui apenas o poster e o artigo publico. Como nem todos os dados experimentais completos estao disponiveis para divulgacao, o primeiro MVP usa dados sinteticos.

Esses dados nao representam medicoes reais de hardware. Eles servem para:

- construir a estrutura do projeto;
- praticar SQL;
- praticar analise com Python;
- montar o dashboard;
- criar a narrativa de portfolio;
- preparar o repositorio para receber dados reais no futuro.

## Principios Usados Na Geracao

Os dados sinteticos seguem os sinais qualitativos descritos no artigo:

- quanto maior `K`, maior tende a ser o erro;
- quanto maior `K`, maior tende a ser a economia de area e energia;
- `LOA` tende a ser mais precisa;
- `TRUNC` tende a economizar mais area e energia, mas com maior erro;
- `COPY` tende a ficar entre `LOA` e `TRUNC`;
- configuracoes com mais bits em `M` e `L` tendem a preservar mais qualidade;
- apenas 30 arquiteturas M-AxPPA sao marcadas como selecionadas para sintese, seguindo a ideia de reduzir o espaco de busca.

## Cuidados De Interpretacao

Os resultados iniciais devem ser descritos como:

> resultados sinteticos para demonstracao de analise.

Evite afirmar:

> esta arquitetura realmente possui X% de economia.

Use:

> no dataset sintetico, esta arquitetura aparece como melhor candidata sob este criterio.

Quando dados reais puderem ser divulgados, esta metodologia deve ser atualizada.

