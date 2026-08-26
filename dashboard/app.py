from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"
HYBRID_VARIANTS_PATH = ROOT / "data" / "processed" / "hybrid_variants_accuracy.csv"
MAXPPA_COMPLETE_RESULTS_PATH = (
    ROOT / "data" / "processed" / "maxppa_complete_results.csv"
)
DEFAULT_MAX_MRED = 0.10
DEFAULT_MAXPPA_MAX_MRED = 0.50
CORE_LSB_VARIANTS = ["COPY", "TRUNC", "LOA"]

VARIANT_COLORS = {
    "APROX5": "#0F766E",
    "AxPPA": "#2563EB",
    "COPY": "#1E3A8A",
    "COPY B": "#92400E",
    "COPY AB": "#2563EB",
    "COPY BA": "#059669",
    "ETA": "#0EA5E9",
    "HEAA": "#84CC16",
    "HERLOA": "#F97316",
    "HOAANED": "#BE123C",
    "HOERRA": "#DC2626",
    "HOERAA": "#EA580C",
    "LDCA": "#86198F",
    "LOA": "#DB2777",
    "LZTA": "#7C3AED",
    "MHEAA": "#16A34A",
    "MHERLOA": "#A16207",
    "M-AxPPA-COPY": "#D97706",
    "M-AxPPA-COPY_B": "#92400E",
    "M-AxPPA-COPY_AB": "#2563EB",
    "M-AxPPA-COPY_BA": "#059669",
    "M-AxPPA-LOA": "#E11D48",
    "M-AxPPA-TRUNC": "#0F766E",
    "M-HEAA": "#16A34A",
    "OLOCA": "#0891B2",
    "SETA": "#4F46E5",
    "TRUNC": "#0891B2",
    "TRUNC 1": "#475569",
}

HYBRID_VARIANT_ORDER = [
    "COPY",
    "LOA",
    "TRUNC",
    "COPY B",
    "COPY AB",
    "COPY BA",
    "TRUNC 1",
    "LZTA",
    "HOERAA",
    "MHEAA",
    "HERLOA",
    "HEAA",
    "ETA",
    "SETA",
    "OLOCA",
    "MHERLOA",
    "LDCA",
    "HOAANED",
]

MAXPPA_VARIANT_ORDER = [
    "APROX5",
    "COPY",
    "ETA",
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
    "HEAA",
]

MAXPPA_METRICS = {
    "PPA gain (%)": "ppa_gain_pct",
    "Power reduction (%)": "total_power_reduction_pct",
    "Area reduction (%)": "total_area_reduction_pct",
    "Energy reduction (%)": "energy_reduction_pct",
    "PDP reduction (%)": "pdp_reduction_pct",
    "Critical delay (ns)": "critical_delay_ns",
    "Exact accuracy (%)": "exact_accuracy_pct",
    "Error (MRED)": "mred",
}

MAXPPA_METRIC_LABELS = {
    "ppa_gain_pct": "Composite PPA gain (%)",
    "total_power_reduction_pct": "Total power reduction (%)",
    "total_area_reduction_pct": "Total area reduction (%)",
    "energy_reduction_pct": "Energy reduction (%)",
    "pdp_reduction_pct": "PDP reduction (%)",
    "critical_delay_ns": "Critical delay (ns)",
    "exact_accuracy_pct": "Exact accuracy (%)",
    "mred": "Error (MRED)",
}

LOWER_IS_BETTER_METRICS = {"mred", "critical_delay_ns", "energy_per_operation_fJ", "pdp_fJ"}


st.set_page_config(
    page_title="M-AxPPA Trade-off Explorer",
    layout="wide",
)


st.markdown(
    """
    <style>
    #MainMenu,
    footer,
    header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }

    .stApp {
        background: #f4f6f8;
        color: #1f2937;
    }

    .block-container {
        max-width: 1720px;
        padding: 1.05rem 2rem 2rem 2rem;
    }

    .hero {
        text-align: center;
        margin-bottom: 0.85rem;
    }

    .hero h1 {
        color: #1f2937;
        font-size: 2.1rem;
        font-weight: 650;
        letter-spacing: 0;
        line-height: 1.1;
        margin: 0 0 0.45rem 0;
    }

    .hero p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }

    .insight-line {
        color: #475569;
        font-size: 0.92rem;
        margin: 0 0 0.75rem 0;
        text-align: center;
    }

    .panel-title {
        color: #1f2937;
        font-size: 1rem;
        font-weight: 750;
        margin: 0 0 0.15rem 0;
    }

    .panel-note {
        color: #64748b;
        font-size: 0.82rem;
        line-height: 1.35;
        margin: 0 0 0.7rem 0;
    }

    .filter-title {
        color: #1f2937;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.45rem 0;
    }

    .filter-note {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.35;
        margin: -0.1rem 0 0.75rem 0;
    }

    .filter-divider {
        border-top: 1px solid #d8dee8;
        margin: 0.75rem 0;
    }

    .variant-dot-wrap {
        align-items: center;
        display: flex;
        min-height: 1.9rem;
        padding-top: 0.08rem;
    }

    .variant-filter-dot {
        border: 1px solid #ffffff;
        border-radius: 999px;
        box-shadow: 0 0 0 1px #cbd5e1;
        display: inline-block;
        height: 0.8rem;
        width: 0.8rem;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        min-height: 106px;
        padding: 0.85rem 1rem;
    }

    .metric-label {
        color: #1f2937;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #111827;
        font-size: 1.78rem;
        font-weight: 720;
        line-height: 1.15;
    }

    .metric-detail {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 0.18rem;
    }

    .chart-panel {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        padding: 0.75rem 0.85rem 0.65rem 0.85rem;
    }

    .chart-title {
        color: #1f2937;
        font-size: 1rem;
        font-weight: 750;
        margin: 0 0 0.12rem 0;
    }

    .chart-subtitle {
        color: #64748b;
        font-size: 0.82rem;
        margin: 0 0 0.55rem 0;
    }

    .legend-title {
        color: #1f2937;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
    }

    .legend-grid {
        display: grid;
        gap: 0.18rem 0.75rem;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .legend-item {
        align-items: center;
        color: #334155;
        display: flex;
        font-size: 0.84rem;
        gap: 0.45rem;
        min-height: 1.25rem;
    }

    .legend-dot {
        border-radius: 999px;
        display: inline-block;
        flex: 0 0 auto;
        height: 0.72rem;
        width: 0.72rem;
    }

    .decision-strip {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        color: #475569;
        font-size: 0.84rem;
        line-height: 1.42;
        margin-top: 0.8rem;
        padding: 0.75rem 0.9rem;
    }

    .footer-note {
        border-top: 1px solid #d8dee8;
        color: #64748b;
        font-size: 0.82rem;
        line-height: 1.45;
        margin-top: 1.35rem;
        padding-top: 0.8rem;
        text-align: center;
    }

    .audit-warning {
        background: #fff7cc;
        border: 1px solid #d97706;
        border-radius: 8px;
        color: #713f12;
        font-size: 0.95rem;
        line-height: 1.45;
        margin: 0.9rem 0 1rem 0;
        padding: 0.85rem 1rem;
    }

    .audit-warning strong {
        color: #713f12;
    }

    [data-testid="stAlert"],
    [data-testid="stAlert"] * {
        color: #111827 !important;
    }

    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
    }

    .stDataFrame {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
    }

    [data-testid="stCheckbox"] label p {
        color: #334155 !important;
        font-size: 0.88rem !important;
    }

    [data-testid="stMultiSelect"] label,
    [data-testid="stMultiSelect"] label p {
        color: #334155 !important;
        font-size: 0.88rem !important;
    }

    [data-testid="stSlider"] label,
    [data-testid="stSlider"] label p,
    [data-testid="stSlider"] p {
        color: #334155 !important;
        font-size: 0.86rem !important;
    }

    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label p,
    [data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #111827 !important;
    }

    [data-testid="stCheckbox"] {
        margin-bottom: -0.35rem;
    }

    [data-baseweb="tab-list"] {
        gap: 0.45rem;
        margin-top: 0.9rem;
    }

    [data-baseweb="tab"] {
        color: #334155;
        font-weight: 650;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb;
    }

    [data-testid="stPlotlyChart"] .modebar {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DATASET_PATH)


@st.cache_data
def load_hybrid_variants() -> pd.DataFrame:
    if not HYBRID_VARIANTS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(HYBRID_VARIANTS_PATH).sort_values(["config_index", "variant"])


@st.cache_data
def load_maxppa_complete_results() -> pd.DataFrame:
    if not MAXPPA_COMPLETE_RESULTS_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(MAXPPA_COMPLETE_RESULTS_PATH).sort_values(
        ["variant", "config_index"]
    )
    df["lsb_strategy"] = df["variant"]
    df["lsb_group"] = df["variant"].apply(classify_lsb_group)
    return df


def classify_lsb_group(variant: str) -> str:
    if variant in CORE_LSB_VARIANTS:
        return "Core LSB: COPY / TRUNC / LOA"
    if variant == "HEAA":
        return "Incomplete audit: HEAA"
    return "Experimental LSB approximators"


def render_metric_card(label: str, value: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_legend(variants: list[str]) -> None:
    items = "\n".join(
        f"""
        <div class="legend-item">
          <span class="legend-dot" style="background:{VARIANT_COLORS.get(variant, '#64748B')}"></span>
          <span>{variant}</span>
        </div>
        """
        for variant in variants
    )
    st.markdown(
        f"""
        <div>
          <div class="legend-title">Variant colors</div>
          <div class="legend-grid">{items}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_scatter(
    data: pd.DataFrame,
    y: str,
    y_label: str,
    selected_variants: list[str],
    x_limit: float,
) -> px.scatter:
    fig = px.scatter(
        data,
        x="mred",
        y=y,
        color="variant",
        color_discrete_map=VARIANT_COLORS,
        category_orders={"variant": selected_variants},
        hover_data={
            "family": True,
            "variant": True,
            "m_bits": True,
            "l_bits": True,
            "k_bits": True,
            "mred": ":.4f",
            y: ":.2f",
            "balanced_score": ":.3f",
        },
    )
    fig.update_traces(
        marker={
            "size": 8.5,
            "opacity": 0.92,
            "line": {"width": 0.55, "color": "#ffffff"},
        }
    )
    fig.update_layout(
        height=350,
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(color="#1f2937", family="Segoe UI"),
    )
    fig.update_xaxes(
        title="Error (MRED)",
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
        range=[0, max(0.01, x_limit)],
    )
    fig.update_yaxes(
        title=y_label,
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
        range=[0, 105],
    )
    return fig


def build_hybrid_variant_line(data: pd.DataFrame, y: str, y_label: str) -> px.line:
    fig = px.line(
        data,
        x="config_index",
        y=y,
        color="variant",
        color_discrete_map=VARIANT_COLORS,
        category_orders={"variant": HYBRID_VARIANT_ORDER},
        log_x=True,
        hover_data={
            "variant": True,
            "m_bits": True,
            "l_bits": True,
            "k_bits": True,
            "ssim": ":.6f",
            "ssim_error": ":.6f",
        },
    )
    fig.update_traces(line={"width": 2.15})
    fig.update_layout(
        height=430,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=8, r=8, t=8, b=8),
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "title": None,
            "font": {"color": "#111827", "size": 10},
        },
        font=dict(color="#1f2937", family="Segoe UI"),
    )
    fig.update_xaxes(
        title="Configuration index",
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    fig.update_yaxes(
        title=y_label,
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    return fig


def build_maxppa_complete_scatter(
    data: pd.DataFrame,
    y: str,
    y_label: str,
    selected_variants: list[str],
    show_legend: bool = False,
) -> px.scatter:
    fig = px.scatter(
        data,
        x="mred",
        y=y,
        color="variant",
        color_discrete_map=VARIANT_COLORS,
        category_orders={"variant": selected_variants},
        hover_data={
            "architecture": True,
            "variant": True,
            "lsb_group": True,
            "m_bits": True,
            "l_bits": True,
            "k_bits": True,
            "mred": ":.6f",
            y: ":.3f",
            "ppa_gain_pct": ":.2f",
        },
    )
    fig.update_traces(
        marker={
            "size": 7.5,
            "opacity": 0.86,
            "line": {"width": 0.45, "color": "#ffffff"},
        }
    )
    fig.update_layout(
        height=390,
        showlegend=show_legend,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(color="#1f2937", family="Segoe UI"),
    )
    fig.update_xaxes(
        title="Error (MRED)",
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    fig.update_yaxes(
        title=y_label,
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    return fig


def build_maxppa_rank_bar(data: pd.DataFrame, metric: str, label: str) -> px.bar:
    top = sort_by_metric(data, metric).head(15).copy()
    top["label"] = top.apply(
        lambda row: (
            f"{row['variant']} | M={int(row['m_bits'])}, "
            f"L={int(row['l_bits'])}, K={int(row['k_bits'])}"
        ),
        axis=1,
    )
    fig = px.bar(
        top,
        x=metric,
        y="label",
        color="variant",
        color_discrete_map=VARIANT_COLORS,
        category_orders={"variant": MAXPPA_VARIANT_ORDER},
        orientation="h",
        hover_data={
            "architecture": True,
            "mred": ":.6f",
            "total_power_reduction_pct": ":.2f",
            "total_area_reduction_pct": ":.2f",
            "critical_delay_ns": ":.3f",
            "ppa_gain_pct": ":.2f",
        },
    )
    fig.update_layout(
        height=520,
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=8, r=8, t=8, b=8),
        yaxis={"categoryorder": "total ascending"},
        font=dict(color="#1f2937", family="Segoe UI"),
    )
    fig.update_xaxes(
        title=label,
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    fig.update_yaxes(title="", tickfont={"color": "#475569", "size": 11})
    return fig


def mark_pareto_candidates(
    data: pd.DataFrame,
    saving_metric: str,
    error_metric: str = "mred",
) -> pd.Series:
    if data.empty:
        return pd.Series(dtype=bool)

    ordered = data.sort_values([error_metric, saving_metric], ascending=[True, False])
    best_seen = -float("inf")
    pareto_flags = []

    for value in ordered[saving_metric]:
        is_candidate = value > best_seen
        pareto_flags.append(is_candidate)
        if value > best_seen:
            best_seen = value

    pareto = pd.Series(False, index=data.index)
    pareto.loc[ordered.index] = pareto_flags
    return pareto


def format_count(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def sort_by_metric(data: pd.DataFrame, metric: str) -> pd.DataFrame:
    return data.sort_values(
        metric,
        ascending=metric in LOWER_IS_BETTER_METRICS,
    )


def select_chart_rows(
    data: pd.DataFrame,
    display_mode: str,
    ranking_metric: str,
    top_n: int,
) -> pd.DataFrame:
    if data.empty or display_mode == "All filtered architectures":
        return data.copy()

    if display_mode == "Pareto candidates only":
        pareto_input = data.copy()
        pareto_metric = ranking_metric
        if ranking_metric in LOWER_IS_BETTER_METRICS:
            pareto_metric = "_pareto_value"
            pareto_input[pareto_metric] = -pareto_input[ranking_metric]
        pareto = mark_pareto_candidates(pareto_input, pareto_metric)
        return data[pareto].copy()

    ranked = sort_by_metric(data, ranking_metric)
    if display_mode == "Best architecture per variant":
        return ranked.groupby("variant", observed=True).head(1).copy()

    return ranked.head(top_n).copy()


def build_lsb_trio_line(
    data: pd.DataFrame,
    metric: str,
    metric_label: str,
) -> px.line:
    ordered = data.sort_values(["config_index", "variant"]).copy()
    fig = px.line(
        ordered,
        x="config_index",
        y=metric,
        color="variant",
        markers=True,
        color_discrete_map=VARIANT_COLORS,
        category_orders={"variant": CORE_LSB_VARIANTS},
        hover_data={
            "variant": True,
            "m_bits": True,
            "l_bits": True,
            "k_bits": True,
            "mred": ":.6f",
            "total_power_reduction_pct": ":.2f",
            "total_area_reduction_pct": ":.2f",
            "ppa_gain_pct": ":.2f",
        },
    )
    fig.update_traces(line={"width": 2.2}, marker={"size": 6})
    fig.update_layout(
        height=430,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=8, r=8, t=8, b=8),
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "title": None,
            "font": {"color": "#111827", "size": 11},
        },
        font=dict(color="#1f2937", family="Segoe UI"),
    )
    fig.update_xaxes(
        title="Configuration index",
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    fig.update_yaxes(
        title=metric_label,
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    return fig


def build_lsb_config_bar(data: pd.DataFrame, metric: str, metric_label: str) -> px.bar:
    ranked = sort_by_metric(data, metric)
    fig = px.bar(
        ranked,
        x="variant",
        y=metric,
        color="variant",
        color_discrete_map=VARIANT_COLORS,
        category_orders={"variant": CORE_LSB_VARIANTS},
        hover_data={
            "architecture": True,
            "m_bits": True,
            "l_bits": True,
            "k_bits": True,
            "mred": ":.6f",
            "total_power_reduction_pct": ":.2f",
            "total_area_reduction_pct": ":.2f",
            "ppa_gain_pct": ":.2f",
        },
    )
    fig.update_layout(
        height=360,
        showlegend=False,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(color="#1f2937", family="Segoe UI"),
    )
    fig.update_xaxes(
        title="LSB approximation",
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    fig.update_yaxes(
        title=metric_label,
        title_font={"color": "#1f2937", "size": 12},
        tickfont={"color": "#475569", "size": 11},
        gridcolor="#dfe4ec",
        zeroline=False,
    )
    return fig


def architecture_label(row: pd.Series) -> str:
    if row["family"] == "M-AxPPA":
        return (
            f"{row['variant']} | M={int(row['m_bits'])}, "
            f"L={int(row['l_bits'])}, K={int(row['k_bits'])}"
        )
    return f"{row['variant']} | K={int(row['k_bits'])}"


if not MAXPPA_COMPLETE_RESULTS_PATH.exists():
    st.error(
        "Complete M-AxPPA dataset not found. Run: "
        "python scripts/prepare_maxppa_complete_results.py"
    )
    st.stop()


legacy_df = load_data()
hybrid_variants_df = load_hybrid_variants()
maxppa_complete_df = load_maxppa_complete_results()

incomplete_variants = (
    maxppa_complete_df[maxppa_complete_df["complete_variant"] == 0]
    .groupby("variant")[["observed_configurations", "expected_configurations"]]
    .first()
    .reset_index()
)

st.markdown(
    """
    <div class="hero">
      <h1>M-AxPPA Complete Trade-off Explorer</h1>
      <p>Extracted synthesis results | Exact MSBs (M), AxPPA intermediate bits (L), approximated LSBs (K)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="insight-line">
    Each point represents one architecture. The best region is upper-left:
    lower error and higher reduction versus the precise baseline.
    </p>
    """,
    unsafe_allow_html=True,
)

variant_col, content_col = st.columns([0.72, 3.35], gap="large")

with variant_col:
    with st.container(border=True):
        st.markdown('<p class="filter-title">M-AxPPA variants</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="filter-note">Main charts use the complete extracted synthesis table.</p>',
            unsafe_allow_html=True,
        )

        if not incomplete_variants.empty:
            details = ", ".join(
                f"{row.variant}: {int(row.observed_configurations)}/"
                f"{int(row.expected_configurations)}"
                for row in incomplete_variants.itertuples(index=False)
            )
            st.markdown(
                '<div class="audit-warning">'
                "<strong>Audit note:</strong> incomplete variants stay out of the "
                f"main view by default. Current incomplete set: {details}."
                "</div>",
                unsafe_allow_html=True,
            )

        show_incomplete = st.checkbox(
            "Include incomplete variants",
            value=False,
            help=(
                "HEAA is currently incomplete because 11 configurations were not "
                "synthesized; keep it off for complete-only comparisons."
            ),
        )

        maxppa_base = maxppa_complete_df.copy()
        if not show_incomplete:
            maxppa_base = maxppa_base[
                maxppa_base["included_in_dashboard"] == 1
            ].copy()

        lsb_group_options = [
            group
            for group in [
                "Core LSB: COPY / TRUNC / LOA",
                "Experimental LSB approximators",
                "Incomplete audit: HEAA",
            ]
            if group in set(maxppa_base["lsb_group"])
        ]
        selected_lsb_groups = st.multiselect(
            "LSB approximation group",
            options=lsb_group_options,
            default=[
                group for group in [
                    "Core LSB: COPY / TRUNC / LOA",
                    "Experimental LSB approximators",
                ]
                if group in lsb_group_options
            ],
            help=(
                "Use this to compare the LSB approximator family. COPY, TRUNC "
                "and LOA are the core M-AxPPA choices."
            ),
        )
        if not selected_lsb_groups:
            selected_lsb_groups = lsb_group_options

        grouped_base = maxppa_base[
            maxppa_base["lsb_group"].isin(selected_lsb_groups)
        ].copy()

        max_mred_limit = float(round(max(maxppa_base["mred"].max(), 0.01) + 0.01, 2))
        max_mred = st.slider(
            "Maximum MRED",
            min_value=0.00,
            max_value=max_mred_limit,
            value=min(DEFAULT_MAXPPA_MAX_MRED, max_mred_limit),
            step=0.01,
            format="%.2f",
            help="Lower this limit when you want stricter error tolerance.",
        )

        st.markdown('<div class="filter-divider"></div>', unsafe_allow_html=True)

        maxppa_available = [
            variant
            for variant in MAXPPA_VARIANT_ORDER
            if variant in set(grouped_base["variant"])
        ]
        preset = st.selectbox(
            "Variant preset",
            [
                "COPY × TRUNC × LOA",
                "All selected groups",
                "Experimental only",
                "Custom selection",
            ],
            help="Quickly switch between a clean LSB comparison and the full architecture set.",
        )
        if preset == "COPY × TRUNC × LOA":
            default_variants = [
                variant for variant in CORE_LSB_VARIANTS if variant in maxppa_available
            ]
        elif preset == "Experimental only":
            default_variants = [
                variant
                for variant in maxppa_available
                if variant not in CORE_LSB_VARIANTS
            ]
        else:
            default_variants = maxppa_available

        selected_maxppa_variants = st.multiselect(
            "Individual variants",
            options=maxppa_available,
            default=default_variants,
            key=f"maxppa_variants_{preset}",
            help="Add/remove specific LSB approximators from the main charts.",
        )
        if not selected_maxppa_variants:
            selected_maxppa_variants = default_variants or maxppa_available

        render_legend(selected_maxppa_variants)

        with st.expander("Bit partition filters", expanded=False):
            m_options = sorted(grouped_base["m_bits"].dropna().astype(int).unique())
            l_options = sorted(grouped_base["l_bits"].dropna().astype(int).unique())
            k_options = sorted(grouped_base["k_bits"].dropna().astype(int).unique())

            selected_m_values = st.multiselect(
                "Exact MSB values (M)",
                options=m_options,
                default=m_options,
            )
            selected_l_values = st.multiselect(
                "AxPPA intermediate values (L)",
                options=l_options,
                default=l_options,
            )
            selected_k_values = st.multiselect(
                "Approximated LSB values (K)",
                options=k_options,
                default=k_options,
            )

        if not selected_m_values:
            selected_m_values = m_options
        if not selected_l_values:
            selected_l_values = l_options
        if not selected_k_values:
            selected_k_values = k_options

        with st.expander("Reduction filters", expanded=False):
            min_power_reduction = st.slider(
                "Minimum power reduction (%)",
                min_value=float(grouped_base["total_power_reduction_pct"].min()),
                max_value=float(grouped_base["total_power_reduction_pct"].max()),
                value=float(grouped_base["total_power_reduction_pct"].min()),
                step=1.0,
            )
            min_area_reduction = st.slider(
                "Minimum area reduction (%)",
                min_value=float(grouped_base["total_area_reduction_pct"].min()),
                max_value=float(grouped_base["total_area_reduction_pct"].max()),
                value=float(grouped_base["total_area_reduction_pct"].min()),
                step=1.0,
            )
            min_ppa_gain = st.slider(
                "Minimum PPA gain (%)",
                min_value=float(grouped_base["ppa_gain_pct"].min()),
                max_value=float(grouped_base["ppa_gain_pct"].max()),
                value=float(grouped_base["ppa_gain_pct"].min()),
                step=1.0,
            )

        st.markdown('<div class="filter-divider"></div>', unsafe_allow_html=True)

        primary_metric_label = st.selectbox(
            "Primary ranking metric",
            options=list(MAXPPA_METRICS.keys()),
            index=0,
        )
        primary_metric = MAXPPA_METRICS[primary_metric_label]

        graph_display_mode = st.radio(
            "Graph density",
            [
                "Best architecture per variant",
                "Top N architectures",
                "Pareto candidates only",
                "All filtered architectures",
            ],
            index=1,
        )
        top_n = st.slider(
            "Top N plotted",
            min_value=10,
            max_value=500,
            value=120,
            step=10,
            help="Used when graph density is set to Top N.",
        )
        left_metric_label = st.selectbox(
            "Left chart metric",
            options=list(MAXPPA_METRICS.keys()),
            index=1,
        )
        right_metric_label = st.selectbox(
            "Right chart metric",
            options=list(MAXPPA_METRICS.keys()),
            index=2,
        )
        left_metric = MAXPPA_METRICS[left_metric_label]
        right_metric = MAXPPA_METRICS[right_metric_label]
        show_graph_legend = st.checkbox("Show chart legend", value=False)

if not selected_maxppa_variants:
    selected_maxppa_variants = maxppa_available

filtered_by_structure = grouped_base[
    grouped_base["m_bits"].isin(selected_m_values)
    & grouped_base["l_bits"].isin(selected_l_values)
    & grouped_base["k_bits"].isin(selected_k_values)
    & (grouped_base["mred"] <= max_mred)
    & (grouped_base["total_power_reduction_pct"] >= min_power_reduction)
    & (grouped_base["total_area_reduction_pct"] >= min_area_reduction)
    & (grouped_base["ppa_gain_pct"] >= min_ppa_gain)
].copy()

maxppa_view = filtered_by_structure[
    filtered_by_structure["variant"].isin(selected_maxppa_variants)
].copy()
maxppa_view["variant"] = pd.Categorical(
    maxppa_view["variant"],
    categories=MAXPPA_VARIANT_ORDER,
    ordered=True,
)

chart_view = select_chart_rows(
    maxppa_view,
    graph_display_mode,
    primary_metric,
    top_n,
)
chart_view["variant"] = pd.Categorical(
    chart_view["variant"],
    categories=MAXPPA_VARIANT_ORDER,
    ordered=True,
)

lsb_trio_view = filtered_by_structure[
    filtered_by_structure["variant"].isin(CORE_LSB_VARIANTS)
].copy()
lsb_trio_view["variant"] = pd.Categorical(
    lsb_trio_view["variant"],
    categories=CORE_LSB_VARIANTS,
    ordered=True,
)

with content_col:
    metric_col_1, metric_col_2, metric_col_3, metric_col_4, metric_col_5 = st.columns(
        5,
        gap="large",
    )
    with metric_col_1:
        if maxppa_view.empty:
            render_metric_card("Displayed Architectures", "0", "No rows match filters")
        else:
            render_metric_card(
                "Filtered Architectures",
                format_count(len(maxppa_view)),
                "Rows matching all filters",
            )

    with metric_col_2:
        if maxppa_view.empty:
            render_metric_card("Plotted Points", "-", "Adjust filters")
        else:
            render_metric_card(
                "Plotted Points",
                format_count(len(chart_view)),
                graph_display_mode,
            )

    with metric_col_3:
        if maxppa_view.empty:
            render_metric_card("Variants", "-", "Adjust filters")
        else:
            render_metric_card(
                "Variants",
                str(maxppa_view["variant"].nunique()),
                "Selected approximators",
            )

    with metric_col_4:
        if maxppa_view.empty:
            render_metric_card("Best Metric", "-", "Adjust filters")
        else:
            best_metric_value = sort_by_metric(maxppa_view, primary_metric).iloc[0][
                primary_metric
            ]
            render_metric_card(
                "Best Metric",
                f"{best_metric_value:.4f}"
                if primary_metric == "mred"
                else f"{best_metric_value:.2f}",
                primary_metric_label,
            )

    with metric_col_5:
        if maxppa_view.empty:
            render_metric_card("Lowest MRED", "-", "Adjust filters")
        else:
            render_metric_card(
                "Lowest MRED",
                f"{maxppa_view['mred'].min():.6f}",
                "Best observed error shown",
            )

    if maxppa_view.empty:
        st.warning("No architectures match the selected filters.")
    else:
        power_col, area_col = st.columns(2, gap="large")

        with power_col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <p class="chart-title">{MAXPPA_METRIC_LABELS[left_metric]} vs Error (MRED)</p>
                    <p class="chart-subtitle">Main view from extracted M-AxPPA synthesis reports. Display mode: {graph_display_mode}.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_maxppa_complete_scatter(
                        chart_view,
                        left_metric,
                        MAXPPA_METRIC_LABELS[left_metric],
                        selected_maxppa_variants,
                        show_graph_legend,
                    ),
                )

        with area_col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <p class="chart-title">{MAXPPA_METRIC_LABELS[right_metric]} vs Error (MRED)</p>
                    <p class="chart-subtitle">Main view from extracted M-AxPPA synthesis reports. Display mode: {graph_display_mode}.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_maxppa_complete_scatter(
                        chart_view,
                        right_metric,
                        MAXPPA_METRIC_LABELS[right_metric],
                        selected_maxppa_variants,
                        show_graph_legend,
                    ),
                )

if not maxppa_view.empty:
    tab_names = ["LSB Trio Compare", "Rankings", "Pareto", "Synthesis Details"]
    if not hybrid_variants_df.empty:
        tab_names.append("MATLAB Hybrid Accuracy")
    if not legacy_df.empty:
        tab_names.append("Legacy Synthetic Data")

    tabs = dict(zip(tab_names, st.tabs(tab_names)))
    lsb_trio_tab = tabs["LSB Trio Compare"]
    ranking_tab = tabs["Rankings"]
    pareto_tab = tabs["Pareto"]
    synthesis_tab = tabs["Synthesis Details"]
    hybrid_tab = tabs.get("MATLAB Hybrid Accuracy")
    legacy_tab = tabs.get("Legacy Synthetic Data")

    with lsb_trio_tab:
        st.info(
            "Direct comparison of the three core M-AxPPA LSB choices: COPY, "
            "TRUNC and LOA. This tab uses the same M/L/K, MRED and reduction "
            "filters, but always focuses on the LSB trio."
        )
        if lsb_trio_view.empty:
            st.warning("No COPY/TRUNC/LOA rows match the current filters.")
        else:
            trio_metric_label = st.selectbox(
                "Metric for COPY × TRUNC × LOA comparison",
                options=list(MAXPPA_METRICS.keys()),
                index=list(MAXPPA_METRICS.keys()).index(primary_metric_label),
            )
            trio_metric = MAXPPA_METRICS[trio_metric_label]

            trio_line_col, trio_config_col = st.columns(2, gap="large")
            with trio_line_col:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p class="chart-title">COPY × TRUNC × LOA across configurations</p>
                        <p class="chart-subtitle">Same bit-partition filters; changing only the LSB approximator.</p>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.plotly_chart(
                        build_lsb_trio_line(
                            lsb_trio_view,
                            trio_metric,
                            MAXPPA_METRIC_LABELS[trio_metric],
                        )
                    )

            config_table = (
                lsb_trio_view[["config_index", "m_bits", "l_bits", "k_bits"]]
                .drop_duplicates()
                .sort_values(["m_bits", "l_bits", "k_bits"])
            )
            config_labels = {
                f"M={int(row.m_bits)}, L={int(row.l_bits)}, K={int(row.k_bits)}"
                f" | config {int(row.config_index)}": int(row.config_index)
                for row in config_table.itertuples(index=False)
            }
            default_config_label = next(iter(config_labels))
            selected_config_label = st.selectbox(
                "Choose one M/L/K split for side-by-side bars",
                options=list(config_labels.keys()),
                index=list(config_labels.keys()).index(default_config_label),
            )
            selected_config = config_labels[selected_config_label]
            selected_config_rows = lsb_trio_view[
                lsb_trio_view["config_index"] == selected_config
            ].copy()

            with trio_config_col:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p class="chart-title">Selected split: {selected_config_label}</p>
                        <p class="chart-subtitle">Side-by-side result for COPY, TRUNC and LOA.</p>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.plotly_chart(
                        build_lsb_config_bar(
                            selected_config_rows,
                            trio_metric,
                            MAXPPA_METRIC_LABELS[trio_metric],
                        )
                    )

            st.dataframe(
                lsb_trio_view[
                    [
                        "architecture",
                        "variant",
                        "config_index",
                        "m_bits",
                        "l_bits",
                        "k_bits",
                        "mred",
                        "total_power_reduction_pct",
                        "total_area_reduction_pct",
                        "critical_delay_ns",
                        "ppa_gain_pct",
                    ]
                ].sort_values(["config_index", "variant"]),
                width="stretch",
                hide_index=True,
            )

    with ranking_tab:
        ranking_metric_complete = st.radio(
            "Ranking criterion",
            [
                "ppa_gain_pct",
                "total_power_reduction_pct",
                "total_area_reduction_pct",
                "energy_reduction_pct",
                "pdp_reduction_pct",
            ],
            horizontal=True,
        )
        ranking_labels = {
            "ppa_gain_pct": "Composite PPA gain (%)",
            "total_power_reduction_pct": "Total power reduction (%)",
            "total_area_reduction_pct": "Total area reduction (%)",
            "energy_reduction_pct": "Energy reduction (%)",
            "pdp_reduction_pct": "PDP reduction (%)",
        }
        st.plotly_chart(
            build_maxppa_rank_bar(
                maxppa_view,
                ranking_metric_complete,
                ranking_labels[ranking_metric_complete],
            ),
        )

    with pareto_tab:
        pareto_power = maxppa_view[mark_pareto_candidates(
            maxppa_view,
            "total_power_reduction_pct",
        )]
        pareto_area = maxppa_view[mark_pareto_candidates(
            maxppa_view,
            "total_area_reduction_pct",
        )]

        pareto_power_col, pareto_area_col = st.columns(2, gap="large")
        with pareto_power_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <p class="chart-title">Power Pareto Candidates</p>
                    <p class="chart-subtitle">Diamonds mark architectures not dominated by lower error and higher power reduction.</p>
                    """,
                    unsafe_allow_html=True,
                )
                fig_pareto_power = build_maxppa_complete_scatter(
                    maxppa_view,
                    "total_power_reduction_pct",
                    "Total power reduction (%)",
                    selected_maxppa_variants,
                )
                fig_pareto_power.update_traces(opacity=0.28)
                fig_pareto_power.add_scatter(
                    x=pareto_power["mred"],
                    y=pareto_power["total_power_reduction_pct"],
                    mode="markers",
                    marker={"size": 11, "symbol": "diamond", "color": "#111827"},
                    name="Pareto candidate",
                )
                st.plotly_chart(fig_pareto_power)

        with pareto_area_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <p class="chart-title">Area Pareto Candidates</p>
                    <p class="chart-subtitle">Diamonds mark architectures not dominated by lower error and higher area reduction.</p>
                    """,
                    unsafe_allow_html=True,
                )
                fig_pareto_area = build_maxppa_complete_scatter(
                    maxppa_view,
                    "total_area_reduction_pct",
                    "Total area reduction (%)",
                    selected_maxppa_variants,
                )
                fig_pareto_area.update_traces(opacity=0.28)
                fig_pareto_area.add_scatter(
                    x=pareto_area["mred"],
                    y=pareto_area["total_area_reduction_pct"],
                    mode="markers",
                    marker={"size": 11, "symbol": "diamond", "color": "#111827"},
                    name="Pareto candidate",
                )
                st.plotly_chart(fig_pareto_area)

    with synthesis_tab:
        st.info(
            "This is the canonical table used by the dashboard opening view: "
            "M exact bits, L AxPPA bits, K approximated bits, plus synthesis "
            "metrics for area, power, timing, energy, PDP and composite PPA gain."
        )

        delay_col, summary_col = st.columns(2, gap="large")
        with delay_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <p class="chart-title">Critical Delay vs Error</p>
                    <p class="chart-subtitle">Timing report metric extracted per architecture.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_maxppa_complete_scatter(
                        maxppa_view,
                        "critical_delay_ns",
                        "Critical delay (ns)",
                        selected_maxppa_variants,
                    ),
                )

        with summary_col:
            with st.container(border=True):
                summary = (
                    maxppa_view.groupby("variant", observed=True)
                    .agg(
                        lsb_group=("lsb_group", "first"),
                        architectures=("architecture", "count"),
                        min_mred=("mred", "min"),
                        max_power_reduction_pct=(
                            "total_power_reduction_pct",
                            "max",
                        ),
                        max_area_reduction_pct=(
                            "total_area_reduction_pct",
                            "max",
                        ),
                        max_ppa_gain_pct=("ppa_gain_pct", "max"),
                    )
                    .reset_index()
                    .sort_values("max_ppa_gain_pct", ascending=False)
                )
                st.markdown(
                    """
                    <p class="chart-title">Variant Summary</p>
                    <p class="chart-subtitle">Aggregated over the current filters.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.dataframe(summary, width="stretch", hide_index=True)

        table_columns = [
            "architecture",
            "variant",
            "lsb_group",
            "config_index",
            "m_bits",
            "l_bits",
            "k_bits",
            "mred",
            "exact_accuracy_pct",
            "total_power_reduction_pct",
            "total_area_reduction_pct",
            "critical_delay_ns",
            "energy_per_operation_fJ",
            "pdp_fJ",
            "ppa_gain_pct",
            "included_in_dashboard",
        ]
        st.dataframe(
            maxppa_view[table_columns].sort_values(
                "ppa_gain_pct", ascending=False
            ),
            width="stretch",
            hide_index=True,
        )

    if hybrid_tab is not None:
        with hybrid_tab:
            st.info(
                "These MATLAB results use the M-AxPPA hybrid structure: exact most-significant bits (M), "
                "AxPPA in the intermediate bits (L), and the selected approximation in the least-significant bits (K)."
            )
            hybrid_available = [
                variant
                for variant in HYBRID_VARIANT_ORDER
                if variant in set(hybrid_variants_df["variant"])
            ]
            selected_hybrid_variants = st.multiselect(
                "Hybrid variants",
                options=hybrid_available,
                default=hybrid_available,
                help="TRUNC B, TRUNC AB and TRUNC BA were removed because they duplicate the COPY variants.",
            )
            if not selected_hybrid_variants:
                selected_hybrid_variants = hybrid_available

            hybrid_view = hybrid_variants_df[
                hybrid_variants_df["variant"].isin(selected_hybrid_variants)
            ].copy()
            hybrid_view["variant"] = pd.Categorical(
                hybrid_view["variant"],
                categories=HYBRID_VARIANT_ORDER,
                ordered=True,
            )

            accuracy_col, error_col = st.columns(2, gap="large")
            with accuracy_col:
                with st.container(border=True):
                    st.markdown(
                        """
                        <p class="chart-title">M-AxPPA Hybrid Accuracy</p>
                        <p class="chart-subtitle">MATLAB SSIM exported from main.m using exact MSBs, AxPPA intermediate bits and approximated LSBs.</p>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.plotly_chart(
                        build_hybrid_variant_line(hybrid_view, "ssim", "SSIM"),
                    )

            with error_col:
                with st.container(border=True):
                    st.markdown(
                        """
                        <p class="chart-title">M-AxPPA Hybrid Error</p>
                        <p class="chart-subtitle">Error computed as 1 - SSIM.</p>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.plotly_chart(
                        build_hybrid_variant_line(hybrid_view, "ssim_error", "1 - SSIM"),
                    )

            st.dataframe(
                hybrid_view.sort_values(["config_index", "variant"]),
                width="stretch",
                hide_index=True,
            )

    if legacy_tab is not None:
        with legacy_tab:
            st.info(
                "Legacy reference only: this synthetic dataset was the original "
                "portfolio/demo view. It is no longer the source for the main "
                "opening charts."
            )
            legacy_variants = sorted(legacy_df["variant"].unique())
            selected_legacy_variants = st.multiselect(
                "Legacy variants",
                options=legacy_variants,
                default=legacy_variants,
            )
            if not selected_legacy_variants:
                selected_legacy_variants = legacy_variants

            legacy_max_mred = st.slider(
                "Legacy maximum MRED",
                min_value=0.00,
                max_value=0.30,
                value=DEFAULT_MAX_MRED,
                step=0.01,
                format="%.2f",
            )
            legacy_filtered = legacy_df[
                legacy_df["variant"].isin(selected_legacy_variants)
                & (legacy_df["mred"] <= legacy_max_mred)
            ].copy()

            if legacy_filtered.empty:
                st.warning("No legacy architectures match the selected filters.")
            else:
                legacy_energy_col, legacy_area_col = st.columns(2, gap="large")
                with legacy_energy_col:
                    st.plotly_chart(
                        build_scatter(
                            legacy_filtered,
                            "energy_saving_pct",
                            "Energy savings (%)",
                            selected_legacy_variants,
                            legacy_max_mred,
                        ),
                    )
                with legacy_area_col:
                    st.plotly_chart(
                        build_scatter(
                            legacy_filtered,
                            "area_saving_pct",
                            "Area savings (%)",
                            selected_legacy_variants,
                            legacy_max_mred,
                        ),
                    )
                columns = [
                    "family",
                    "variant",
                    "m_bits",
                    "l_bits",
                    "k_bits",
                    "ssim",
                    "ncc",
                    "mae",
                    "mre",
                    "mred",
                    "energy_saving_pct",
                    "area_saving_pct",
                    "balanced_score",
                    "selected_for_synthesis",
                ]
                st.dataframe(
                    legacy_filtered[columns].sort_values(
                        "balanced_score",
                        ascending=False,
                    ),
                    width="stretch",
                    hide_index=True,
                )

st.markdown(
    """
    <div class="footer-note">
    Main dashboard view uses the extracted M-AxPPA synthesis results. Legacy
    synthetic data is kept only as a separate reference/audit tab.
    </div>
    """,
    unsafe_allow_html=True,
)
