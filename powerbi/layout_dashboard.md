# Layout Sugerido Do Dashboard

## Pagina 1 - Visao Geral

Objetivo: mostrar rapidamente o tamanho do estudo e o problema de decisao.

Elementos:

- Cartao: total de arquiteturas.
- Cartao: arquiteturas M-AxPPA.
- Cartao: arquiteturas com `MRED <= 0.10`.
- Cartao: maior economia de energia com erro controlado.
- Cartao: maior economia de area com erro controlado.
- Grafico de dispersao: `mred` vs `energy_saving_pct`, com cor por `variant`.
- Grafico de dispersao: `mred` vs `area_saving_pct`, com cor por `variant`.

Texto curto na pagina:

```text
O objetivo e comparar arquiteturas aproximadas considerando erro, energia e area. A melhor escolha depende da restricao de erro aceita.
```

## Pagina 2 - Ranking De Candidatas

Objetivo: mostrar as melhores arquiteturas sob diferentes criterios.

Elementos:

- Tabela com `variant`, `configuration`, `mred`, `energy_saving_pct`, `area_saving_pct`, `balanced_score`.
- Filtro por `family`.
- Filtro por `variant`.
- Filtro por `error_class`.
- Barras horizontais: top 10 por `energy_saving_pct`.
- Barras horizontais: top 10 por `area_saving_pct`.
- Barras horizontais: top 10 por `balanced_score`.

## Pagina 3 - Trade-off Energia x Erro

Objetivo: explicar que energia maior pode vir com mais erro.

Elementos:

- Grafico de dispersao grande:
  - X: `mred`
  - Y: `energy_saving_pct`
  - Cor: `variant`
  - Tamanho: `area_saving_pct`
- Segmentador para `error_class`.
- Segmentador para `strategy`.

Insight esperado:

```text
Arquiteturas mais agressivas podem economizar mais energia, mas precisam ser avaliadas contra um limite maximo de erro.
```

## Pagina 4 - Trade-off Area x Erro

Objetivo: mostrar que area tambem pode ser otimizada, mas nem sempre com a mesma arquitetura que lidera energia.

Elementos:

- Grafico de dispersao:
  - X: `mred`
  - Y: `area_saving_pct`
  - Cor: `variant`
- Tabela de candidatas com `MRED <= 0.10`.

Insight esperado:

```text
Quando o objetivo muda de energia para area, o ranking das arquiteturas tambem muda.
```

## Pagina 5 - Conclusao

Objetivo: transformar graficos em decisao.

Texto sugerido:

```text
O estudo mostra que a escolha da arquitetura depende de restricoes. Com um limite de erro definido, e possivel ranquear candidatas por economia de energia, economia de area ou score balanceado. Esse fluxo transforma resultados tecnicos de hardware em apoio objetivo para tomada de decisao.
```

Inclua uma tabela final com as melhores candidatas por:

- energia;
- area;
- score balanceado;
- menor erro.

