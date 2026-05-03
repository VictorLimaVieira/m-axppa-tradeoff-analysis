# Approximate Computing Trade-off Explorer

Data analytics project inspired by the public paper **M-AxPPA: Modified Approximate Parallel Prefix Adder**.

The goal is to analyze approximate adder architectures and answer one central question:

> Given an acceptable error threshold, which architectures provide the best energy and area savings?

![Power BI dashboard preview](reports/figures/dashboard_v1.png)

## Project Status

This is a public portfolio V1.

The current dataset is **synthetic** and was generated from the public structure described in the M-AxPPA paper. It is intended to demonstrate the analytics workflow, not to claim real hardware measurements.

Synthetic dataset scope:

- `W = 16` bits;
- 3 M-AxPPA variants: `COPY`, `TRUNC`, and `LOA`;
- 105 `(M, L, K)` configurations per M-AxPPA variant;
- 315 M-AxPPA architectures;
- 128 literature baseline configurations;
- 443 architectures in total;
- accuracy, error, energy, and area metrics prepared for SQL, Python, Power BI, and Streamlit analysis.

## Confidentiality Note

Current unpublished research involving DCT is intentionally excluded from this repository. This project only uses public paper information and clearly labeled synthetic data.

## What This Project Demonstrates

- Experimental data modeling.
- SQL analysis with SQLite.
- Python data generation and preparation.
- Multi-objective trade-off analysis.
- Power BI dashboard design.
- Streamlit interactive dashboard.
- Technical storytelling for data portfolio.

## Main Insight

The best architecture depends on the decision criterion.

An architecture can maximize energy savings but produce too much error. Another can preserve accuracy but save less area. The useful workflow is:

```text
1. Filter architectures by acceptable error.
2. Rank the remaining candidates by energy savings, area savings, or balanced score.
3. Compare architecture families and approximation strategies.
```

## Dashboard

The Power BI dashboard compares:

- error (`MRED`) vs energy savings;
- error (`MRED`) vs area savings;
- displayed architectures after filtering;
- maximum energy savings;
- maximum area savings;
- architecture variants through an interactive slicer.

Power BI file:

```text
powerbi/M_AxPPA_Tradeoff_Dashboard.pbix
```

Power BI dataset:

```text
powerbi/m_axppa_powerbi_dataset.xlsx
```

## Repository Structure

```text
data/
  synthetic/          Synthetic normalized tables
  processed/          Unified processed dataset
database/
  schema.sql          Relational schema
  queries/            SQL analysis queries
dashboard/
  app.py              Streamlit dashboard
docs/
  resumo_do_artigo.md
  metodologia_dados_sinteticos.md
powerbi/
  M_AxPPA_Tradeoff_Dashboard.pbix
  m_axppa_powerbi_dataset.xlsx
  theme_m_axppa_tradeoff.json
portfolio/
  estudo_de_caso_v1.md
  curriculo_linkedin.md
src/
  data_generation/
    generate_synthetic_data.py
  prepare_powerbi_dataset.py
  run_query.py
reports/
  figures/
    dashboard_v1.png
```

## How To Generate The Data

```bash
python src/data_generation/generate_synthetic_data.py
```

This creates:

- `data/synthetic/architectures.csv`
- `data/synthetic/accuracy_metrics.csv`
- `data/synthetic/synthesis_metrics.csv`
- `data/processed/tradeoff_dataset.csv`
- `database/m_axppa_synthetic.sqlite`

## How To Prepare The Power BI Dataset

```bash
python src/prepare_powerbi_dataset.py
```

This creates:

- `powerbi/m_axppa_powerbi_dataset.csv`
- `powerbi/m_axppa_powerbi_dataset.xlsx`
- `powerbi/resultados_resumo.csv`
- `powerbi/resultados_resumo.xlsx`

## How To Run SQL Queries

Example:

```bash
python src/run_query.py database/queries/02_energia_com_erro_controlado.sql
```

Example question:

> Which architectures maximize energy savings while keeping `MRED <= 0.10`?

## How To Run The Streamlit Dashboard

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run dashboard/app.py
```

## Tools

- Python
- Pandas
- SQLite
- SQL
- Power BI
- Streamlit
- Plotly

## Limitations

The current values are synthetic and should not be interpreted as real hardware measurements.

The project is designed to demonstrate the data workflow and can be extended with real experimental data if public disclosure becomes possible.

## Next Steps

- Deploy the Streamlit dashboard.
- Add Python notebooks for exploratory data analysis.
- Add Pareto frontier analysis.
- Improve the Power BI dashboard with a second page for ranking.
- Translate supporting documentation to English.

