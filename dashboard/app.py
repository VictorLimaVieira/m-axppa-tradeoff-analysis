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
    return pd.read_csv(MAXPPA_COMPLETE_RESULTS_PATH).sort_values(
        ["variant", "config_index"]
    )


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
    top = data.sort_values(metric, ascending=False).head(15).copy()
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

        max_mred = st.slider(
            "Maximum MRED",
            min_value=0.00,
            max_value=DEFAULT_MAXPPA_MAX_MRED,
            value=DEFAULT_MAXPPA_MAX_MRED,
            step=0.01,
            format="%.2f",
            help="Lower this limit when you want stricter error tolerance.",
        )

        st.markdown('<div class="filter-divider"></div>', unsafe_allow_html=True)

        maxppa_available = [
            variant
            for variant in MAXPPA_VARIANT_ORDER
            if variant in set(maxppa_base["variant"])
        ]
        selected_maxppa_variants = []
        for variant in maxppa_available:
            dot_col, check_col = st.columns([0.14, 0.86], gap="small")
            with dot_col:
                st.markdown(
                    f"""
                    <div class="variant-dot-wrap">
                      <span class="variant-filter-dot" style="background:{VARIANT_COLORS.get(variant, '#64748B')}"></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with check_col:
                if st.checkbox(
                    variant,
                    value=True,
                    key=f"maxppa_variant_{variant}",
                ):
                    selected_maxppa_variants.append(variant)

if not selected_maxppa_variants:
    selected_maxppa_variants = maxppa_available

maxppa_view = maxppa_base[
    maxppa_base["variant"].isin(selected_maxppa_variants)
    & (maxppa_base["mred"] <= max_mred)
].copy()
maxppa_view["variant"] = pd.Categorical(
    maxppa_view["variant"],
    categories=MAXPPA_VARIANT_ORDER,
    ordered=True,
)

with content_col:
    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4, gap="large")
    with metric_col_1:
        if maxppa_view.empty:
            render_metric_card("Displayed Architectures", "0", "No rows match filters")
        else:
            render_metric_card(
                "Displayed Architectures",
                format_count(len(maxppa_view)),
                "M-AxPPA rows after filters",
            )

    with metric_col_2:
        if maxppa_view.empty:
            render_metric_card("Variants", "-", "Adjust filters")
        else:
            render_metric_card(
                "Variants",
                str(maxppa_view["variant"].nunique()),
                "Complete variants by default",
            )

    with metric_col_3:
        if maxppa_view.empty:
            render_metric_card("Best PPA Gain", "-", "Adjust filters")
        else:
            render_metric_card(
                "Best PPA Gain",
                f"{maxppa_view['ppa_gain_pct'].max():.2f}%",
                f"Within MRED <= {max_mred:.2f}",
            )

    with metric_col_4:
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
                    """
                    <p class="chart-title">Power Reduction (%) vs Error (MRED)</p>
                    <p class="chart-subtitle">Updated main view from extracted M-AxPPA synthesis reports.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_maxppa_complete_scatter(
                        maxppa_view,
                        "total_power_reduction_pct",
                        "Total power reduction (%)",
                        selected_maxppa_variants,
                    ),
                )

        with area_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <p class="chart-title">Area Reduction (%) vs Error (MRED)</p>
                    <p class="chart-subtitle">Updated main view from total area reduction versus the precise baseline.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_maxppa_complete_scatter(
                        maxppa_view,
                        "total_area_reduction_pct",
                        "Total area reduction (%)",
                        selected_maxppa_variants,
                    ),
                )

if not maxppa_view.empty:
    tab_names = ["Rankings", "Pareto", "Synthesis Details"]
    if not hybrid_variants_df.empty:
        tab_names.append("MATLAB Hybrid Accuracy")
    if not legacy_df.empty:
        tab_names.append("Legacy Synthetic Data")

    tabs = dict(zip(tab_names, st.tabs(tab_names)))
    ranking_tab = tabs["Rankings"]
    pareto_tab = tabs["Pareto"]
    synthesis_tab = tabs["Synthesis Details"]
    hybrid_tab = tabs.get("MATLAB Hybrid Accuracy")
    legacy_tab = tabs.get("Legacy Synthetic Data")

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
