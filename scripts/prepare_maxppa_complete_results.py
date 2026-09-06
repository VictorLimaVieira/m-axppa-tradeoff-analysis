from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "resultados_completos.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "maxppa_complete_results.csv"

EXPECTED_VARIANTS = [
    "APROX5",
    "COPY",
    "ETA",
    "HEAA",
    "HERLOA",
    "HOAANED",
    "HOERRA",
    "LDCA",
    "LOA",
    "LZTA",
    "MHEAA",
    "MHERLOA",
    "OLOCA",
    "SETA",
    "TRUNC",
]
TOTAL_BITS = 16
EXPECTED_CONFIGS_PER_VARIANT = 105

COLUMN_MAP = {
    "arquitetura": "architecture",
    "somador": "variant",
    "M": "m_bits",
    "L": "l_bits",
    "K": "k_bits",
    "soma_M_L_K": "m_l_k_sum",
    "combinacao_M_L_K_valida": "valid_mlk",
    "baseline_preciso": "baseline_precise",
    "dados_acuracia_presentes": "accuracy_data_present",
    "dados_sintese_presentes": "synthesis_data_present",
    "acuracia_exata_pct": "exact_accuracy_pct",
    "taxa_erro_pct": "error_rate_pct",
    "ME": "mean_error",
    "MAE_MED": "mae",
    "MSE": "mse",
    "RMSE": "rmse",
    "WCE_erro_absoluto_maximo": "wce",
    "MRE_assinado": "mre_signed",
    "MRED": "mred",
    "MAPE_pct": "mape_pct",
    "WCRE": "wcre",
    "NMED_full_scale": "nmed_full_scale",
    "NRMSE_full_scale": "nrmse_full_scale",
    "fidelidade_NMED_pct": "nmed_fidelity_pct",
    "R2": "r2",
    "correlacao_pearson": "pearson_correlation",
    "SNR_dB": "snr_db",
    "PSNR_dB": "psnr_db",
    "cell_count": "cell_count",
    "cell_area_um2": "cell_area_um2",
    "net_area_um2": "net_area_um2",
    "total_area_um2": "total_area_um2",
    "potencia_leakage_uW": "leakage_power_uW",
    "potencia_internal_uW": "internal_power_uW",
    "potencia_switching_uW": "switching_power_uW",
    "potencia_total_uW": "total_power_uW",
    "atraso_critico_ns": "critical_delay_ns",
    "fmax_teorica_MHz": "theoretical_fmax_mhz",
    "energia_por_operacao_fJ": "energy_per_operation_fJ",
    "PDP_fJ": "pdp_fJ",
    "EDP_fJ_ns": "edp_fJ_ns",
    "produto_area_atraso_um2_ns": "area_delay_product_um2_ns",
    "produto_area_potencia_um2_uW": "area_power_product_um2_uW",
    "reducao_cell_count_pct": "cell_count_reduction_pct",
    "reducao_cell_area_pct": "cell_area_reduction_pct",
    "reducao_net_area_pct": "net_area_reduction_pct",
    "reducao_total_area_pct": "total_area_reduction_pct",
    "reducao_leakage_power_pct": "leakage_power_reduction_pct",
    "reducao_internal_power_pct": "internal_power_reduction_pct",
    "reducao_switching_power_pct": "switching_power_reduction_pct",
    "reducao_total_power_pct": "total_power_reduction_pct",
    "reducao_atraso_pct": "delay_reduction_pct",
    "speedup_atraso": "delay_speedup",
    "reducao_energia_operacao_pct": "energy_reduction_pct",
    "reducao_PDP_pct": "pdp_reduction_pct",
    "reducao_ADP_pct": "adp_reduction_pct",
    "PPA_composto_relativo": "ppa_composite_relative",
    "ganho_PPA_composto_pct": "ppa_gain_pct",
}


def expected_configurations() -> pd.DataFrame:
    records = []
    config_index = 1
    for m_bits in range(1, TOTAL_BITS - 1):
        for l_bits in range(1, TOTAL_BITS - m_bits):
            k_bits = TOTAL_BITS - m_bits - l_bits
            records.append(
                {
                    "config_index": config_index,
                    "m_bits": m_bits,
                    "l_bits": l_bits,
                    "k_bits": k_bits,
                }
            )
            config_index += 1
    return pd.DataFrame(records)


def normalize_boolish(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0).astype(int)


def prepare(input_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(input_path, sep=";")
    missing_columns = [column for column in COLUMN_MAP if column not in raw.columns]
    if missing_columns:
        raise ValueError(
            "Input CSV is missing required columns: " + ", ".join(missing_columns)
        )

    data = raw[list(COLUMN_MAP)].rename(columns=COLUMN_MAP).copy()

    integer_columns = [
        "m_bits",
        "l_bits",
        "k_bits",
        "m_l_k_sum",
        "valid_mlk",
        "baseline_precise",
        "accuracy_data_present",
        "synthesis_data_present",
    ]
    for column in integer_columns:
        data[column] = normalize_boolish(data[column])

    numeric_columns = [
        column
        for column in data.columns
        if column not in {"architecture", "variant"} and column not in integer_columns
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    approx = data[
        (data["baseline_precise"] == 0)
        & (data["valid_mlk"] == 1)
        & (data["accuracy_data_present"] == 1)
        & (data["synthesis_data_present"] == 1)
    ].copy()

    configs = expected_configurations()
    approx = approx.merge(configs, on=["m_bits", "l_bits", "k_bits"], how="left")

    counts = approx.groupby("variant").size().rename("observed_configurations")
    data = data.merge(counts, on="variant", how="left")
    approx = approx.merge(counts, on="variant", how="left")

    approx["observed_configurations"] = (
        approx["observed_configurations"].fillna(0).astype(int)
    )
    approx["expected_configurations"] = EXPECTED_CONFIGS_PER_VARIANT
    approx["complete_variant"] = (
        approx["observed_configurations"] == EXPECTED_CONFIGS_PER_VARIANT
    ).astype(int)
    approx["included_in_dashboard"] = approx["complete_variant"]

    ordered_columns = [
        "architecture",
        "variant",
        "config_index",
        "m_bits",
        "l_bits",
        "k_bits",
        "m_l_k_sum",
        "valid_mlk",
        "accuracy_data_present",
        "synthesis_data_present",
        "observed_configurations",
        "expected_configurations",
        "complete_variant",
        "included_in_dashboard",
        "exact_accuracy_pct",
        "error_rate_pct",
        "mean_error",
        "mae",
        "mse",
        "rmse",
        "wce",
        "mre_signed",
        "mred",
        "mape_pct",
        "wcre",
        "nmed_full_scale",
        "nrmse_full_scale",
        "nmed_fidelity_pct",
        "r2",
        "pearson_correlation",
        "snr_db",
        "psnr_db",
        "cell_count",
        "cell_area_um2",
        "net_area_um2",
        "total_area_um2",
        "leakage_power_uW",
        "internal_power_uW",
        "switching_power_uW",
        "total_power_uW",
        "critical_delay_ns",
        "theoretical_fmax_mhz",
        "energy_per_operation_fJ",
        "pdp_fJ",
        "edp_fJ_ns",
        "area_delay_product_um2_ns",
        "area_power_product_um2_uW",
        "cell_count_reduction_pct",
        "cell_area_reduction_pct",
        "net_area_reduction_pct",
        "total_area_reduction_pct",
        "leakage_power_reduction_pct",
        "internal_power_reduction_pct",
        "switching_power_reduction_pct",
        "total_power_reduction_pct",
        "delay_reduction_pct",
        "delay_speedup",
        "energy_reduction_pct",
        "pdp_reduction_pct",
        "adp_reduction_pct",
        "ppa_composite_relative",
        "ppa_gain_pct",
    ]
    approx = approx[ordered_columns].sort_values(["variant", "config_index"])

    summary = (
        approx.groupby("variant", as_index=False)
        .agg(
            observed_configurations=("architecture", "count"),
            included_in_dashboard=("included_in_dashboard", "max"),
            min_mred=("mred", "min"),
            median_mred=("mred", "median"),
            max_power_reduction_pct=("total_power_reduction_pct", "max"),
            max_area_reduction_pct=("total_area_reduction_pct", "max"),
            max_ppa_gain_pct=("ppa_gain_pct", "max"),
        )
        .sort_values("variant")
    )
    summary["expected_configurations"] = EXPECTED_CONFIGS_PER_VARIANT
    summary["missing_configurations"] = (
        summary["expected_configurations"] - summary["observed_configurations"]
    )

    expected = expected_configurations()
    missing_records = []
    for variant in EXPECTED_VARIANTS:
        observed = set(
            approx.loc[
                approx["variant"] == variant, ["m_bits", "l_bits", "k_bits"]
            ].itertuples(index=False, name=None)
        )
        for row in expected.itertuples(index=False):
            key = (row.m_bits, row.l_bits, row.k_bits)
            if key not in observed:
                missing_records.append(
                    {
                        "variant": variant,
                        "config_index": row.config_index,
                        "m_bits": row.m_bits,
                        "l_bits": row.l_bits,
                        "k_bits": row.k_bits,
                    }
                )
    missing = pd.DataFrame(missing_records)

    return approx, summary, missing


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare complete M-AxPPA synthesis/accuracy results for Streamlit."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=(
            "Path to resultados_completos.csv. Defaults to "
            "data/raw/resultados_completos.csv when no path is provided."
        ),
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=None,
        help="Optional path for a variant-level summary CSV.",
    )
    parser.add_argument(
        "--missing-output",
        type=Path,
        default=None,
        help="Optional path for missing M/L/K configurations.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    approx, summary, missing = prepare(args.input)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    approx.to_csv(args.output, index=False)

    if args.summary_output is not None:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(args.summary_output, index=False)

    if args.missing_output is not None:
        args.missing_output.parent.mkdir(parents=True, exist_ok=True)
        missing.to_csv(args.missing_output, index=False)

    included = int(approx["included_in_dashboard"].sum())
    excluded = int((approx["included_in_dashboard"] == 0).sum())
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Rows prepared: {len(approx)}")
    print(f"Rows included in dashboard by default: {included}")
    print(f"Rows excluded from the default dashboard view: {excluded}")
    print("Variant summary:")
    print(
        summary[
            [
                "variant",
                "observed_configurations",
                "expected_configurations",
                "missing_configurations",
                "included_in_dashboard",
            ]
        ].to_string(index=False)
    )
    if args.missing_output is not None and not missing.empty:
        print(f"Missing configurations written to: {args.missing_output}")


if __name__ == "__main__":
    main()
