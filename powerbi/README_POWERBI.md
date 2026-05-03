# Dashboard Power BI - M-AxPPA

Este diretorio contem os arquivos para criar uma primeira versao do dashboard no Power BI.

## Arquivos

- `m_axppa_powerbi_dataset.csv`: dataset principal para importar no Power BI.
- `m_axppa_powerbi_dataset.xlsx`: versao em Excel do dataset principal. Recomendada se o Power BI interpretar decimais do CSV de forma errada.
- `resultados_resumo.csv`: rankings prontos para consulta rapida.
- `resultados_resumo.xlsx`: versao em Excel dos rankings.
- `medidas_dax.md`: medidas DAX recomendadas.
- `layout_dashboard.md`: roteiro visual das paginas do dashboard.

## Importacao No Power BI

1. Abra o Power BI Desktop.
2. Clique em **Obter dados**.
3. Escolha **Excel workbook**.
4. Importe:

```text
powerbi/m_axppa_powerbi_dataset.xlsx
```

5. Confirme se as colunas numericas foram reconhecidas como numeros decimais ou inteiros.
6. Clique em **Carregar**.

## Primeira Pagina Recomendada

Nome da pagina:

```text
Visao Geral
```

Crie estes cartoes:

- Total de arquiteturas.
- Media de economia de energia.
- Media de economia de area.
- Menor MRED.
- Quantidade de arquiteturas com `MRED <= 0.10`.

Crie estes graficos:

- Dispersao: `mred` no eixo X e `energy_saving_pct` no eixo Y.
- Dispersao: `mred` no eixo X e `area_saving_pct` no eixo Y.
- Barras: top arquiteturas por `balanced_score`.

Use `variant` como legenda/cor.

## Mensagem Principal Do Dashboard

O dashboard deve mostrar que a melhor arquitetura depende da restricao escolhida.

Se o objetivo e energia, uma arquitetura pode liderar. Se o objetivo e area, outra pode aparecer melhor. Se o objetivo e erro baixo, o ranking muda novamente.

Essa e a historia de dados do projeto:

> Filtrar arquiteturas por erro aceitavel e, dentro desse conjunto, ranquear por economia de energia, area ou score balanceado.

## Observacao Para GitHub

Como os dados sao sinteticos, deixe claro no README e no dashboard:

```text
Dados sinteticos baseados na estrutura publica do artigo M-AxPPA. Os valores sao usados para demonstracao de analise e nao representam medicoes reais de hardware.
```
