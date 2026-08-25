# M-AxPPA Complete Results Pipeline

This project has two M-AxPPA data paths:

1. a synthetic portfolio dataset used by the original dashboard views;
2. a complete MATLAB/synthesis extraction dataset generated from the professor's reports.

The complete-results path follows this flow:

```text
automatico3.py
    -> generates VHDL architectures

simulation/synthesis tools
    -> generate accuracy, area, power, timing and cell reports

reports.zip
    -> stores the raw report files

extrair_resultados_maxppa.py
    -> extracts raw reports into resultados_completos.csv

scripts/prepare_maxppa_complete_results.py
    -> prepares a clean dashboard-ready CSV

data/processed/maxppa_complete_results.csv
    -> feeds the Streamlit "Complete M-AxPPA Results" tab
```

## File roles

- `automatico3.py`: source generator for the pure M-AxPPA VHDL variants. It
  defines the supported approximate low-significant-bit strategies and writes
  architectures named as `M_AxPPA_<variant>_M#_L#_K#`.
- `reports.zip`: raw simulation and synthesis output. This is the audit source,
  not the ideal dashboard input.
- `extrair_resultados_maxppa.py`: parser/extractor for the raw reports. It
  creates `resultados_completos.csv`, `resultados_celulas.csv`, and a missing
  results report.
- `resultados_completos.csv`: extracted table containing accuracy and synthesis
  metrics per architecture.
- `scripts/prepare_maxppa_complete_results.py`: repository automation that
  filters and normalizes `resultados_completos.csv` for Streamlit.

## Current completeness rule

The scripts define 15 approximate strategies and 105 `(M, L, K)` combinations
per strategy, so a complete set is 1,575 approximate architectures.

The current extracted CSV contains 1,564 approximate architectures. `HEAA` has
94 of the expected 105 configurations, so the dashboard keeps those rows for
audit but excludes `HEAA` from the complete-results charts by default.

Generated dashboard files:

- `data/processed/maxppa_complete_results.csv`
- `data/processed/maxppa_complete_summary.csv`
- `data/processed/maxppa_missing_configurations.csv`

To refresh the processed Streamlit data after receiving a new
`resultados_completos.csv`, run:

```bash
python scripts/prepare_maxppa_complete_results.py
```
