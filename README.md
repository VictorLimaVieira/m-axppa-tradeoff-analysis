# M-AxPPA Trade-off Dashboard

Dashboard interativo para análise de somadores aproximados baseados na estrutura M-AxPPA.

O objetivo é comparar arquiteturas por erro, potência, área, atraso, energia, PDP e ganho PPA composto, permitindo recortes por regiões de bits:

- `M`: bits mais significativos mantidos exatos;
- `L`: bits intermediários avaliados com AxPPA;
- `K`: bits menos significativos avaliados pela aproximação selecionada.

## Dashboard online

[Abrir dashboard](https://m-axppa-tradeoff-analysis.streamlit.app/)

## Dados usados pelo dashboard

O Streamlit usa dois arquivos processados:

```text
data/processed/maxppa_complete_results.csv
data/processed/hybrid_variants_accuracy.csv
```

O primeiro arquivo contém as métricas principais de síntese e acurácia das arquiteturas M-AxPPA. O segundo contém a comparação de acurácia exportada do MATLAB para os híbridos avaliados durante o desenvolvimento.

## Estrutura do projeto

```text
dashboard/
  app.py

data/
  processed/
    maxppa_complete_results.csv
    hybrid_variants_accuracy.csv

scripts/
  prepare_maxppa_complete_results.py

streamlit_app.py
requirements.txt
```

## Como rodar localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o dashboard:

```bash
streamlit run streamlit_app.py
```

## Como atualizar os resultados

Quando houver um novo arquivo `resultados_completos.csv`, gere novamente a tabela processada:

```bash
python scripts/prepare_maxppa_complete_results.py --input "caminho/para/resultados_completos.csv"
```

O script atualiza:

```text
data/processed/maxppa_complete_results.csv
```

## Observação sobre acesso aos dados

Enquanto o repositório GitHub estiver público e o dashboard Streamlit carregar arquivos CSV do próprio repositório, os arquivos necessários ao funcionamento do dashboard também ficam acessíveis no GitHub.

Para restringir de fato o acesso aos dados, use uma destas alternativas:

- manter o repositório privado;
- carregar os dados a partir de uma fonte privada;
- configurar os dados como segredo/arquivo privado no ambiente de deploy.

No estado atual, a interface pública prioriza gráficos e resumos, sem expor tabelas completas linha a linha.
