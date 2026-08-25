from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"
HYBRID_VARIANTS_PATH = ROOT / "data" / "processed" / "hybrid_variants_accuracy.csv"
DEFAULT_MAX_MRED = 0.10

VARIANT_COLORS = {
    "AxPPA": "#2563EB",
    "COPY": "#1E3A8A",
    "COPY B": "#92400E",
    "COPY AB": "#2563EB",
    "COPY BA": "#059669",
    "ETA": "#0EA5E9",
    "HEAA": "#84CC16",
    "HERLOA": "#F97316",
    "HOAANED": "#BE123C",
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
    return pd.read_csv(DATASET_PATH)


@st.cache_data
def load_hybrid_variants() -> pd.DataFrame:
    if not HYBRID_VARIANTS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(HYBRID_VARIANTS_PATH).sort_values(["config_index", "variant"])


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


def architecture_label(row: pd.Series) -> str:
    if row["family"] == "M-AxPPA":
        return (
            f"{row['variant']} | M={int(row['m_bits'])}, "
            f"L={int(row['l_bits'])}, K={int(row['k_bits'])}"
        )
    return f"{row['variant']} | K={int(row['k_bits'])}"


if not DATASET_PATH.exists():
    st.error(
        "Dataset not found. Run: python src/data_generation/generate_synthetic_data.py"
    )
    st.stop()


df = load_data()
hybrid_variants_df = load_hybrid_variants()
all_variants = sorted(df["variant"].unique())

st.markdown(
    """
    <div class="hero">
      <h1>Approximate Computing Trade-off Explorer</h1>
      <p>Synthetic M-AxPPA dataset | Error, energy and area analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="insight-line">
    Each point represents one architecture. The best region is upper-left:
    lower error and higher savings.
    </p>
    """,
    unsafe_allow_html=True,
)

variant_col, content_col = st.columns([0.72, 3.35], gap="large")

with variant_col:
    with st.container(border=True):
        st.markdown('<p class="filter-title">Variant</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="filter-note">Select the architecture variants shown in the charts.</p>',
            unsafe_allow_html=True,
        )
        selected_variants = []
        for variant in all_variants:
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
                if st.checkbox(variant, value=True, key=f"variant_{variant}"):
                    selected_variants.append(variant)
        st.markdown('<div class="filter-divider"></div>', unsafe_allow_html=True)
        max_mred = st.slider(
            "Maximum MRED",
            min_value=0.00,
            max_value=0.30,
            value=DEFAULT_MAX_MRED,
            step=0.01,
            format="%.2f",
            help="Use a lower limit for stricter error tolerance.",
        )

if not selected_variants:
    selected_variants = all_variants

filtered = df[
    df["variant"].isin(selected_variants)
    & (df["mred"] <= max_mred)
].copy()

with content_col:
    metric_col_1, metric_col_2, metric_col_3 = st.columns(3, gap="large")
    with metric_col_1:
        if filtered.empty:
            render_metric_card("Displayed Architectures", "0", "No rows match filters")
        else:
            render_metric_card(
                "Displayed Architectures",
                f"{len(filtered):,.0f}",
                "Architectures after current filters",
            )

    with metric_col_2:
        if filtered.empty:
            render_metric_card("Maximum Energy Savings", "-", "Adjust filters")
        else:
            render_metric_card(
                "Maximum Energy Savings",
                f"{filtered['energy_saving_pct'].max():.2f}%",
                f"Within MRED <= {max_mred:.2f}",
            )

    with metric_col_3:
        if filtered.empty:
            render_metric_card("Maximum Area Savings", "-", "Adjust filters")
        else:
            render_metric_card(
                "Maximum Area Savings",
                f"{filtered['area_saving_pct'].max():.2f}%",
                f"Within MRED <= {max_mred:.2f}",
            )

    if filtered.empty:
        st.warning("No architectures match the selected filters.")
    else:
        energy_col, area_col = st.columns(2, gap="large")

        with energy_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <p class="chart-title">Energy Savings (%) vs Error (MRED)</p>
                    <p class="chart-subtitle">Energy view: controlled error with higher power reduction.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_scatter(
                        filtered,
                        "energy_saving_pct",
                        "Energy savings (%)",
                        selected_variants,
                        max_mred,
                    ),
                    use_container_width=True,
                )

        with area_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <p class="chart-title">Area Savings (%) vs Error (MRED)</p>
                    <p class="chart-subtitle">Area view: controlled error with smaller circuit footprint.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    build_scatter(
                        filtered,
                        "area_saving_pct",
                        "Area savings (%)",
                        selected_variants,
                        max_mred,
                    ),
                    use_container_width=True,
                )

if not filtered.empty:
    if hybrid_variants_df.empty:
        ranking_tab, pareto_tab, data_tab = st.tabs(["Rankings", "Pareto", "Data"])
        hybrid_tab = None
    else:
        ranking_tab, pareto_tab, hybrid_tab, data_tab = st.tabs(
            ["Rankings", "Pareto", "M-AxPPA MATLAB Hybrids", "Data"]
        )

    with ranking_tab:
        ranking_metric = st.radio(
            "Ranking criterion",
            ["balanced_score", "energy_saving_pct", "area_saving_pct", "mred"],
            horizontal=True,
        )
        ascending = ranking_metric == "mred"
        top = filtered.sort_values(ranking_metric, ascending=ascending).head(15).copy()
        top["label"] = top.apply(architecture_label, axis=1)

        fig_rank = px.bar(
            top,
            x=ranking_metric,
            y="label",
            color="variant",
            color_discrete_map=VARIANT_COLORS,
            category_orders={"variant": selected_variants},
            orientation="h",
            title=f"Top architectures by {ranking_metric}",
        )
        fig_rank.update_layout(
            height=540,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            margin=dict(l=10, r=10, t=52, b=10),
            legend={
                "title": {"font": {"color": "#111827", "size": 12}},
                "font": {"color": "#111827", "size": 11},
            },
            yaxis={"categoryorder": "total ascending"},
            font=dict(color="#1f2937", family="Segoe UI"),
        )
        fig_rank.update_xaxes(
            gridcolor="#dfe4ec",
            title_font={"color": "#111827", "size": 12},
            tickfont={"color": "#111827", "size": 11},
        )
        fig_rank.update_yaxes(title="", tickfont={"color": "#111827", "size": 11})
        st.plotly_chart(fig_rank, use_container_width=True)

    with pareto_tab:
        pareto = filtered[
            (filtered["pareto_optimal_energy_error"] == 1)
            | (filtered["pareto_optimal_area_error"] == 1)
        ]
        fig_pareto = build_scatter(
            filtered,
            "energy_saving_pct",
            "Energy savings (%)",
            selected_variants,
            max_mred,
        )
        fig_pareto.update_traces(opacity=0.35)
        fig_pareto.add_scatter(
            x=pareto["mred"],
            y=pareto["energy_saving_pct"],
            mode="markers",
            marker={"size": 11, "symbol": "diamond", "color": "#111827"},
            name="Pareto candidate",
        )
        st.plotly_chart(fig_pareto, use_container_width=True)

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
                        use_container_width=True,
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
                        use_container_width=True,
                    )

            st.dataframe(
                hybrid_view.sort_values(["config_index", "variant"]),
                use_container_width=True,
                hide_index=True,
            )

    with data_tab:
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
            filtered[columns].sort_values("balanced_score", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

st.markdown(
    """
    <div class="footer-note">
    Synthetic data based on the public M-AxPPA paper structure. Values demonstrate
    the analysis workflow and do not represent real hardware measurements.
    </div>
    """,
    unsafe_allow_html=True,
)
