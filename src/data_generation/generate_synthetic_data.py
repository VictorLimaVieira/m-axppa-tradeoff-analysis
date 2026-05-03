from __future__ import annotations

import csv
import math
import random
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC_DIR = ROOT / "data" / "synthetic"
PROCESSED_DIR = ROOT / "data" / "processed"
DATABASE_PATH = ROOT / "database" / "m_axppa_synthetic.sqlite"
SCHEMA_PATH = ROOT / "database" / "schema.sql"

RANDOM_SEED = 42
W_BITS = 16
INPUT_VECTORS = 1_000_000

SELECTED_MLK = {
    (1, 7, 8),
    (1, 14, 1),
    (2, 1, 13),
    (3, 1, 12),
    (4, 1, 11),
    (6, 5, 5),
    (7, 4, 5),
    (8, 3, 5),
    (10, 1, 5),
    (12, 1, 3),
}

M_AXPPA_VARIANTS = ("COPY", "TRUNC", "LOA")
LITERATURE_BASELINES = (
    "COPY",
    "LOA",
    "TRUNC",
    "LDCA",
    "LZTA",
    "M-HEAA",
    "AxPPA",
    "HOERAA",
)


@dataclass(frozen=True)
class Architecture:
    architecture_id: int
    family: str
    variant: str
    baseline_source: str
    w_bits: int
    m_bits: int | None
    l_bits: int | None
    k_bits: int
    approximation_strategy: str
    is_literature_baseline: int
    selected_for_synthesis: int


@dataclass(frozen=True)
class AccuracyMetrics:
    architecture_id: int
    input_vectors: int
    ssim: float
    ncc: float
    mae: float
    mre: float
    mred: float
    accuracy_rank: int


@dataclass(frozen=True)
class SynthesisMetrics:
    architecture_id: int
    technology_node_nm: int
    supply_voltage: float
    clock_mhz: int
    energy_saving_pct: float
    area_saving_pct: float
    power_mw: float
    area_um2: float
    delay_ns: float
    pdp: float
    edp: float


@dataclass(frozen=True)
class TradeoffScore:
    architecture_id: int
    normalized_error: float
    normalized_energy_saving: float
    normalized_area_saving: float
    balanced_score: float
    pareto_optimal_energy_error: int
    pareto_optimal_area_error: int


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def jitter(scale: float) -> float:
    return random.uniform(-scale, scale)


def generate_architectures() -> list[Architecture]:
    architectures: list[Architecture] = []
    architecture_id = 1

    for variant in M_AXPPA_VARIANTS:
        for m_bits in range(1, W_BITS - 1):
            for l_bits in range(1, W_BITS - 1):
                k_bits = W_BITS - m_bits - l_bits
                if k_bits < 1:
                    continue

                architectures.append(
                    Architecture(
                        architecture_id=architecture_id,
                        family="M-AxPPA",
                        variant=f"M-AxPPA-{variant}",
                        baseline_source="synthetic_from_public_paper_structure",
                        w_bits=W_BITS,
                        m_bits=m_bits,
                        l_bits=l_bits,
                        k_bits=k_bits,
                        approximation_strategy=variant,
                        is_literature_baseline=0,
                        selected_for_synthesis=int((m_bits, l_bits, k_bits) in SELECTED_MLK),
                    )
                )
                architecture_id += 1

    for baseline in LITERATURE_BASELINES:
        for k_bits in range(1, W_BITS + 1):
            architectures.append(
                Architecture(
                    architecture_id=architecture_id,
                    family="Literature",
                    variant=baseline,
                    baseline_source="synthetic_literature_baseline",
                    w_bits=W_BITS,
                    m_bits=None,
                    l_bits=None,
                    k_bits=k_bits,
                    approximation_strategy=baseline,
                    is_literature_baseline=1,
                    selected_for_synthesis=1,
                )
            )
            architecture_id += 1

    return architectures


def estimate_accuracy(architecture: Architecture) -> tuple[float, float, float, float, float]:
    k_ratio = architecture.k_bits / architecture.w_bits
    l_ratio = (architecture.l_bits or 0) / architecture.w_bits
    m_ratio = (architecture.m_bits or 0) / architecture.w_bits

    m_axppa_mre_factor = {
        "COPY": 0.27,
        "TRUNC": 0.47,
        "LOA": 0.16,
    }
    m_axppa_mred_factor = {
        "COPY": 0.18,
        "TRUNC": 0.294,
        "LOA": 0.108,
    }
    literature_mre_factor = {
        "COPY": 0.34,
        "LOA": 0.22,
        "TRUNC": 0.70,
        "LDCA": 0.28,
        "LZTA": 0.42,
        "M-HEAA": 0.18,
        "AxPPA": 0.12,
        "HOERAA": 0.20,
    }

    if architecture.family == "M-AxPPA":
        strategy = architecture.approximation_strategy
        mre = (k_ratio**2) * m_axppa_mre_factor[strategy]
        mre += l_ratio * 0.0018
        mre += (1 - m_ratio) * 0.0008
        mred = (k_ratio**2) * m_axppa_mred_factor[strategy]
        mred += l_ratio * 0.0007
    else:
        strategy = architecture.approximation_strategy
        mre = (k_ratio**2) * literature_mre_factor[strategy]
        mred = (k_ratio**2) * literature_mre_factor[strategy] * 0.65

        if strategy == "TRUNC" and architecture.k_bits == W_BITS:
            mred = 5_000.0
            mre = 1.0

    mre = clamp(mre + jitter(0.0015), 0.0, 1.0)
    mred = clamp(mred + jitter(0.001), 0.0, 5_000.0)

    ssim = clamp(1 - (mre * 0.45) - (mred * 0.04 if mred < 1 else 0.25), 0.0, 1.0)
    ncc = clamp(1 - (mre * 0.18) - (mred * 0.02 if mred < 1 else 0.15), 0.0, 1.0)
    mae = clamp(mre * 56_500 + architecture.k_bits * 14 + jitter(40), 0.0, 65_535.0)

    # Public values mentioned in the article are used as synthetic anchors.
    if architecture.family == "M-AxPPA" and (architecture.m_bits, architecture.l_bits, architecture.k_bits) == (1, 1, 14):
        if architecture.approximation_strategy == "TRUNC":
            return 0.835, 0.932, 20_460.0, 0.362, mred
        if architecture.approximation_strategy == "COPY":
            return 0.902, 0.948, 12_280.0, 0.208, mred
        if architecture.approximation_strategy == "LOA":
            return 0.920, 0.953, 8_167.0, 0.126, mred

    if architecture.family == "M-AxPPA" and (architecture.m_bits, architecture.l_bits, architecture.k_bits) == (4, 10, 2):
        return 0.9987, 0.9993, 10_300.0, 0.0202, mred

    return round(ssim, 6), round(ncc, 6), round(mae, 3), round(mre, 6), round(mred, 6)


def estimate_synthesis(architecture: Architecture) -> tuple[float, float, float, float, float, float, float]:
    k_ratio = architecture.k_bits / architecture.w_bits
    l_ratio = (architecture.l_bits or 0) / architecture.w_bits

    if architecture.family == "M-AxPPA":
        energy_offset = {
            "TRUNC": 17.0,
            "COPY": 12.0,
            "LOA": 9.0,
        }[architecture.approximation_strategy]
        area_offset = {
            "TRUNC": 23.0,
            "COPY": 10.0,
            "LOA": -1.0,
        }[architecture.approximation_strategy]

        energy_saving = 8 + 85 * k_ratio + 35 * l_ratio * 0.35 + energy_offset
        area_saving = 5 + 63 * k_ratio + 10 * l_ratio + area_offset
    else:
        strategy = architecture.approximation_strategy
        energy_offset = {
            "COPY": 10.0,
            "LOA": 6.0,
            "TRUNC": 20.0,
            "LDCA": 8.0,
            "LZTA": 13.0,
            "M-HEAA": 7.0,
            "AxPPA": 11.0,
            "HOERAA": 5.0,
        }[strategy]
        area_offset = {
            "COPY": 9.0,
            "LOA": 4.0,
            "TRUNC": 27.0,
            "LDCA": 7.0,
            "LZTA": 12.0,
            "M-HEAA": 5.0,
            "AxPPA": 10.0,
            "HOERAA": 4.0,
        }[strategy]
        energy_saving = 6 + 72 * k_ratio + energy_offset
        area_saving = 4 + 58 * k_ratio + area_offset

    energy_saving = clamp(energy_saving + jitter(1.2), 0.0, 98.0)
    area_saving = clamp(area_saving + jitter(1.4), 0.0, 92.0)

    baseline_power_mw = 1.25
    baseline_area_um2 = 1_000.0
    baseline_delay_ns = 5.0

    power_mw = baseline_power_mw * (1 - energy_saving / 100)
    area_um2 = baseline_area_um2 * (1 - area_saving / 100)
    delay_ns = baseline_delay_ns * (1 - clamp(k_ratio * 0.35, 0.0, 0.45))
    pdp = power_mw * delay_ns
    edp = power_mw * delay_ns * delay_ns

    if architecture.family == "M-AxPPA" and (architecture.m_bits, architecture.l_bits, architecture.k_bits) == (2, 1, 13):
        if architecture.approximation_strategy == "TRUNC":
            energy_saving = 96.25
            area_saving = 84.46
        if architecture.approximation_strategy == "LOA":
            energy_saving = 88.62
            area_saving = 60.93

        power_mw = baseline_power_mw * (1 - energy_saving / 100)
        area_um2 = baseline_area_um2 * (1 - area_saving / 100)
        delay_ns = baseline_delay_ns * (1 - clamp(k_ratio * 0.35, 0.0, 0.45))
        pdp = power_mw * delay_ns
        edp = power_mw * delay_ns * delay_ns

    return (
        round(energy_saving, 4),
        round(area_saving, 4),
        round(power_mw, 6),
        round(area_um2, 3),
        round(delay_ns, 6),
        round(pdp, 6),
        round(edp, 6),
    )


def is_pareto_optimal(rows: list[dict], x_key: str, y_key: str) -> dict[int, int]:
    # Lower x is better, higher y is better.
    result: dict[int, int] = {}
    for candidate in rows:
        dominated = False
        for other in rows:
            if other["architecture_id"] == candidate["architecture_id"]:
                continue
            better_or_equal = other[x_key] <= candidate[x_key] and other[y_key] >= candidate[y_key]
            strictly_better = other[x_key] < candidate[x_key] or other[y_key] > candidate[y_key]
            if better_or_equal and strictly_better:
                dominated = True
                break
        result[candidate["architecture_id"]] = int(not dominated)
    return result


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_database(
    architectures: list[Architecture],
    accuracy_metrics: list[AccuracyMetrics],
    synthesis_metrics: list[SynthesisMetrics],
    tradeoff_scores: list[TradeoffScore],
) -> None:
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    connection = sqlite3.connect(DATABASE_PATH)
    with connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.executemany(
            """
            INSERT INTO architectures VALUES (
                :architecture_id, :family, :variant, :baseline_source, :w_bits,
                :m_bits, :l_bits, :k_bits, :approximation_strategy,
                :is_literature_baseline, :selected_for_synthesis
            )
            """,
            [asdict(row) for row in architectures],
        )
        connection.executemany(
            """
            INSERT INTO accuracy_metrics VALUES (
                :architecture_id, :input_vectors, :ssim, :ncc, :mae,
                :mre, :mred, :accuracy_rank
            )
            """,
            [asdict(row) for row in accuracy_metrics],
        )
        connection.executemany(
            """
            INSERT INTO synthesis_metrics VALUES (
                :architecture_id, :technology_node_nm, :supply_voltage,
                :clock_mhz, :energy_saving_pct, :area_saving_pct,
                :power_mw, :area_um2, :delay_ns, :pdp, :edp
            )
            """,
            [asdict(row) for row in synthesis_metrics],
        )
        connection.executemany(
            """
            INSERT INTO tradeoff_scores VALUES (
                :architecture_id, :normalized_error, :normalized_energy_saving,
                :normalized_area_saving, :balanced_score,
                :pareto_optimal_energy_error, :pareto_optimal_area_error
            )
            """,
            [asdict(row) for row in tradeoff_scores],
        )
    connection.close()


def main() -> None:
    random.seed(RANDOM_SEED)

    architectures = generate_architectures()

    raw_accuracy = []
    for architecture in architectures:
        ssim, ncc, mae, mre, mred = estimate_accuracy(architecture)
        raw_accuracy.append(
            {
                "architecture_id": architecture.architecture_id,
                "input_vectors": INPUT_VECTORS,
                "ssim": ssim,
                "ncc": ncc,
                "mae": mae,
                "mre": mre,
                "mred": mred,
            }
        )

    ranked_accuracy = sorted(raw_accuracy, key=lambda row: row["mred"])
    rank_by_id = {
        row["architecture_id"]: index + 1 for index, row in enumerate(ranked_accuracy)
    }
    accuracy_metrics = [
        AccuracyMetrics(**row, accuracy_rank=rank_by_id[row["architecture_id"]])
        for row in raw_accuracy
    ]

    synthesis_metrics = []
    for architecture in architectures:
        energy, area, power, area_um2, delay, pdp, edp = estimate_synthesis(architecture)
        synthesis_metrics.append(
            SynthesisMetrics(
                architecture_id=architecture.architecture_id,
                technology_node_nm=65,
                supply_voltage=1.25,
                clock_mhz=200,
                energy_saving_pct=energy,
                area_saving_pct=area,
                power_mw=power,
                area_um2=area_um2,
                delay_ns=delay,
                pdp=pdp,
                edp=edp,
            )
        )

    accuracy_by_id = {row.architecture_id: row for row in accuracy_metrics}
    synthesis_by_id = {row.architecture_id: row for row in synthesis_metrics}

    max_mred_for_score = max(
        row.mred for row in accuracy_metrics if row.mred < 100
    )
    max_energy = max(row.energy_saving_pct for row in synthesis_metrics)
    max_area = max(row.area_saving_pct for row in synthesis_metrics)

    joined_rows = []
    for architecture in architectures:
        accuracy = accuracy_by_id[architecture.architecture_id]
        synthesis = synthesis_by_id[architecture.architecture_id]
        joined_rows.append(
            {
                **asdict(architecture),
                **asdict(accuracy),
                **asdict(synthesis),
            }
        )

    pareto_energy = is_pareto_optimal(joined_rows, "mred", "energy_saving_pct")
    pareto_area = is_pareto_optimal(joined_rows, "mred", "area_saving_pct")

    tradeoff_scores = []
    for architecture in architectures:
        accuracy = accuracy_by_id[architecture.architecture_id]
        synthesis = synthesis_by_id[architecture.architecture_id]

        normalized_error = 1 - clamp(accuracy.mred / max_mred_for_score, 0.0, 1.0)
        normalized_energy = synthesis.energy_saving_pct / max_energy
        normalized_area = synthesis.area_saving_pct / max_area
        balanced_score = (
            0.45 * normalized_error
            + 0.35 * normalized_energy
            + 0.20 * normalized_area
        )

        tradeoff_scores.append(
            TradeoffScore(
                architecture_id=architecture.architecture_id,
                normalized_error=round(normalized_error, 6),
                normalized_energy_saving=round(normalized_energy, 6),
                normalized_area_saving=round(normalized_area, 6),
                balanced_score=round(balanced_score, 6),
                pareto_optimal_energy_error=pareto_energy[architecture.architecture_id],
                pareto_optimal_area_error=pareto_area[architecture.architecture_id],
            )
        )

    score_by_id = {row.architecture_id: row for row in tradeoff_scores}
    final_rows = []
    for row in joined_rows:
        score = score_by_id[row["architecture_id"]]
        final_rows.append({**row, **asdict(score)})

    write_csv(SYNTHETIC_DIR / "architectures.csv", [asdict(row) for row in architectures])
    write_csv(SYNTHETIC_DIR / "accuracy_metrics.csv", [asdict(row) for row in accuracy_metrics])
    write_csv(SYNTHETIC_DIR / "synthesis_metrics.csv", [asdict(row) for row in synthesis_metrics])
    write_csv(SYNTHETIC_DIR / "tradeoff_scores.csv", [asdict(row) for row in tradeoff_scores])
    write_csv(PROCESSED_DIR / "tradeoff_dataset.csv", final_rows)

    build_database(architectures, accuracy_metrics, synthesis_metrics, tradeoff_scores)

    print("Synthetic M-AxPPA dataset generated.")
    print(f"Architectures: {len(architectures)}")
    print(f"M-AxPPA architectures: {sum(a.family == 'M-AxPPA' for a in architectures)}")
    print(f"Literature baselines: {sum(a.family == 'Literature' for a in architectures)}")
    print(f"SQLite database: {DATABASE_PATH}")


if __name__ == "__main__":
    main()

