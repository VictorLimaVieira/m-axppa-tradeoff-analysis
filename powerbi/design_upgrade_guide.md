# Power BI Design Upgrade Guide

Use este guia para transformar a V1 funcional em uma V1 bonita para portfolio.

## 1. Aplicar Tema

No Power BI:

1. Abra o arquivo `.pbix`.
2. Va em **View**.
3. Clique na seta de **Themes**.
4. Escolha **Browse for themes**.
5. Selecione:

```text
powerbi/theme_m_axppa_tradeoff.json
```

Esse tema aplica uma paleta mais profissional, fundo claro, bordas e cores consistentes.

## 2. Layout Recomendado

Use a pagina em tres zonas:

```text
Topo:
Titulo grande + subtitulo

Esquerda:
Grafico 1 - Energy Savings vs Error
Grafico 2 - Area Savings vs Error

Direita:
3 cards empilhados
Slicer de Variant abaixo dos cards
```

## 3. Fundo Da Pagina

Em uma area vazia da pagina:

1. Clique no fundo.
2. Va em **Format page**.
3. Em **Canvas background**, use:

```text
#F6F7F9
Transparency: 0%
```

Isso tira o branco puro e ajuda os cards a aparecerem.

## 4. Graficos

Para cada grafico:

- Background: branco.
- Border: ligado.
- Border color: `#D9DEE7`.
- Rounded corners/radius: `8`, se aparecer.
- Visual header: desligado.
- Gridlines: cinza claro.
- Titulo: 12 ou 13 px.
- Subtitulo: 9 ou 10 px, cinza.

Titulos:

```text
Energy Savings vs Error
Area Savings vs Error
```

Subtitulo:

```text
Architectures with MRED below 0.25
```

Eixos:

```text
Error (MRED)
Energy savings (%)
Area savings (%)
```

## 5. Cards

Cards recomendados:

```text
Displayed Architectures
Maximum Energy Savings
Maximum Area Savings
```

Estilo:

- Fundo branco.
- Borda ligada.
- Borda `#D9DEE7`.
- Cantos arredondados, se aparecer.
- Valor grande.
- Titulo curto.

Ordem:

```text
Displayed Architectures
Maximum Energy Savings
Maximum Area Savings
```

## 6. Slicer

Transforme `variant` em dropdown se possivel:

1. Clique no slicer.
2. Va em **Format visual**.
3. Procure **Slicer settings**.
4. Em **Style**, escolha **Dropdown**.

Titulo:

```text
Variant
```

Se o dropdown ficar dificil, deixe como lista. Lista tambem funciona.

## 7. Titulo Principal

Titulo:

```text
Approximate Computing Trade-off Dashboard
```

Subtitulo:

```text
Synthetic M-AxPPA dataset | Error, energy and area analysis
```

Estilo:

- Titulo centralizado.
- Tamanho entre 24 e 30.
- Cor `#20242A`.
- Subtitulo em cinza `#475569`.

## 8. Pequena Faixa De Contexto

Opcional, mas deixa o dashboard mais profissional:

Adicione uma caixa de texto pequena no rodape:

```text
Synthetic data based on the public M-AxPPA paper structure. Values demonstrate the analysis workflow and do not represent real hardware measurements.
```

Use fonte 8 ou 9, cinza.

