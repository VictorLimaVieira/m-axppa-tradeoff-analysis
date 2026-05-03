from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"
POWERBI_DIR = ROOT / "powerbi"


def to_float(value: str) -> float:
    if value == "":
        return 0.0
    return float(value)


def to_int(value: str) -> int:
    if value == "":
        return 0
    return int(float(value))


def classify_error(mred: float) -> str:
    if mred <= 0.05:
        return "Baixo erro"
    if mred <= 0.10:
        return "Erro controlado"
    if mred <= 0.25:
        return "Erro moderado"
    return "Erro alto"


def classify_profile(mred: float, energy: float, area: float) -> str:
    if mred <= 0.10 and energy >= 80:
        return "Alta economia com erro controlado"
    if mred <= 0.05:
        return "Prioridade em acuracia"
    if area >= 65 and mred <= 0.15:
        return "Prioridade em area"
    if energy >= 85:
        return "Prioridade em energia"
    return "Trade-off intermediario"


def main() -> None:
    POWERBI_DIR.mkdir(parents=True, exist_ok=True)

    with INPUT_PATH.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    powerbi_rows = []
    for row in rows:
        m_bits = to_int(row["m_bits"])
        l_bits = to_int(row["l_bits"])
        k_bits = to_int(row["k_bits"])
        mred = to_float(row["mred"])
        energy = to_float(row["energy_saving_pct"])
        area = to_float(row["area_saving_pct"])
        balanced_score = to_float(row["balanced_score"])

        powerbi_rows.append(
            {
                "architecture_id": row["architecture_id"],
                "family": row["family"],
                "variant": row["variant"],
                "strategy": row["approximation_strategy"],
                "w_bits": row["w_bits"],
                "m_bits": m_bits,
                "l_bits": l_bits,
                "k_bits": k_bits,
                "configuration": f"M={m_bits}, L={l_bits}, K={k_bits}"
                if row["family"] == "M-AxPPA"
                else f"K={k_bits}",
                "is_literature_baseline": row["is_literature_baseline"],
                "selected_for_synthesis": row["selected_for_synthesis"],
                "ssim": row["ssim"],
                "ncc": row["ncc"],
                "mae": row["mae"],
                "mre": row["mre"],
                "mred": mred,
                "error_class": classify_error(mred),
                "energy_saving_pct": energy,
                "area_saving_pct": area,
                "power_mw": row["power_mw"],
                "area_um2": row["area_um2"],
                "delay_ns": row["delay_ns"],
                "pdp": row["pdp"],
                "edp": row["edp"],
                "balanced_score": balanced_score,
                "profile": classify_profile(mred, energy, area),
                "pareto_energy_error": row["pareto_optimal_energy_error"],
                "pareto_area_error": row["pareto_optimal_area_error"],
                "is_acceptable_mred_010": int(mred <= 0.10),
                "is_acceptable_mred_005": int(mred <= 0.05),
            }
        )

    fieldnames = list(powerbi_rows[0].keys())
    with (POWERBI_DIR / "m_axppa_powerbi_dataset.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(powerbi_rows)

    pd.DataFrame(powerbi_rows).to_excel(
        POWERBI_DIR / "m_axppa_powerbi_dataset.xlsx",
        index=False,
        sheet_name="m_axppa_powerbi_dataset",
    )

    top_energy_controlled = sorted(
        [row for row in powerbi_rows if row["mred"] <= 0.10],
        key=lambda row: row["energy_saving_pct"],
        reverse=True,
    )[:10]

    top_area_controlled = sorted(
        [row for row in powerbi_rows if row["mred"] <= 0.10],
        key=lambda row: row["area_saving_pct"],
        reverse=True,
    )[:10]

    top_balanced = sorted(
        powerbi_rows,
        key=lambda row: row["balanced_score"],
        reverse=True,
    )[:10]

    summary_rows = []
    for ranking_name, ranking_rows in [
        ("Maior economia de energia com MRED <= 0.10", top_energy_controlled),
        ("Maior economia de area com MRED <= 0.10", top_area_controlled),
        ("Maior score balanceado", top_balanced),
    ]:
        for position, row in enumerate(ranking_rows, start=1):
            summary_rows.append(
                {
                    "ranking": ranking_name,
                    "position": position,
                    "family": row["family"],
                    "variant": row["variant"],
                    "configuration": row["configuration"],
                    "mred": row["mred"],
                    "energy_saving_pct": row["energy_saving_pct"],
                    "area_saving_pct": row["area_saving_pct"],
                    "balanced_score": row["balanced_score"],
                }
            )

    with (POWERBI_DIR / "resultados_resumo.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    pd.DataFrame(summary_rows).to_excel(
        POWERBI_DIR / "resultados_resumo.xlsx",
        index=False,
        sheet_name="resultados_resumo",
    )

    print("Power BI dataset generated.")
    print(POWERBI_DIR / "m_axppa_powerbi_dataset.csv")
    print(POWERBI_DIR / "m_axppa_powerbi_dataset.xlsx")
    print(POWERBI_DIR / "resultados_resumo.csv")
    print(POWERBI_DIR / "resultados_resumo.xlsx")


if __name__ == "__main__":
    main()
