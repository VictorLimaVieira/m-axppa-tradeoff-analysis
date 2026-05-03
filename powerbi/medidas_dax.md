# Medidas DAX Sugeridas

Use estas medidas no Power BI depois de importar `m_axppa_powerbi_dataset.csv`.

Substitua o nome da tabela se o Power BI importar com outro nome.

## Medidas Basicas

```DAX
Total Arquiteturas =
COUNTROWS(m_axppa_powerbi_dataset)
```

```DAX
Arquiteturas M-AxPPA =
CALCULATE(
    COUNTROWS(m_axppa_powerbi_dataset),
    m_axppa_powerbi_dataset[family] = "M-AxPPA"
)
```

```DAX
Arquiteturas Com Erro Controlado =
CALCULATE(
    COUNTROWS(m_axppa_powerbi_dataset),
    m_axppa_powerbi_dataset[mred] <= 0.10
)
```

```DAX
Menor MRED =
MIN(m_axppa_powerbi_dataset[mred])
```

```DAX
Media Economia Energia =
AVERAGE(m_axppa_powerbi_dataset[energy_saving_pct])
```

```DAX
Media Economia Area =
AVERAGE(m_axppa_powerbi_dataset[area_saving_pct])
```

```DAX
Maior Score Balanceado =
MAX(m_axppa_powerbi_dataset[balanced_score])
```

## Medidas Para Cartoes Com Filtro De Erro

```DAX
Maior Energia Com MRED 010 =
CALCULATE(
    MAX(m_axppa_powerbi_dataset[energy_saving_pct]),
    m_axppa_powerbi_dataset[mred] <= 0.10
)
```

```DAX
Maior Area Com MRED 010 =
CALCULATE(
    MAX(m_axppa_powerbi_dataset[area_saving_pct]),
    m_axppa_powerbi_dataset[mred] <= 0.10
)
```

```DAX
Percentual Com Erro Controlado =
DIVIDE(
    [Arquiteturas Com Erro Controlado],
    [Total Arquiteturas]
)
```

## Coluna Calculada Opcional

Se quiser criar uma coluna calculada dentro do Power BI:

```DAX
Classe De Decisao =
IF(
    m_axppa_powerbi_dataset[mred] <= 0.10
        && m_axppa_powerbi_dataset[energy_saving_pct] >= 80,
    "Alta economia com erro controlado",
    IF(
        m_axppa_powerbi_dataset[mred] <= 0.05,
        "Prioridade em acuracia",
        "Trade-off intermediario"
    )
)
```

