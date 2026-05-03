from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"

COLOR_SEQUENCE = [
    "#1E88E5",
    "#10A37F",
    "#F59E0B",
    "#E45756",
    "#6D5DF6",
    "#00A6A6",
    "#8E44AD",
    "#64748B",
    "#D946EF",
    "#2F4858",
]

VARIANT_COLORS = {
    "AxPPA": "#1E88E5",
    "COPY": "#2F3A9E",
    "HOERAA": "#F07A3F",
    "LDCA": "#8E1A8C",
    "LOA": "#D946A8",
    "LZTA": "#7E63D6",
    "M-AxPPA-COPY": "#D9A300",
    "M-AxPPA-LOA": "#E45756",
    "M-AxPPA-TRUNC": "#197A80",
    "M-HEAA": "#2FAD66",
    "TRUNC": "#22B8D8",
}

DEFAULT_VARIANTS = [
    "M-AxPPA-COPY",
    "M-AxPPA-LOA",
    "M-AxPPA-TRUNC",
    "AxPPA",
    "LOA",
    "TRUNC",
]


st.set_page_config(
    page_title="M-AxPPA Trade-off Explorer",
    page_icon="",
    layout="wide",
)


st.markdown(
    """
    <style>
    .stApp {
        background: #f6f7f9;
        color: #20242a;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1240px;
    }
    .hero {
        text-align: center;
        margin-bottom: 1.25rem;
    }
    .hero h1 {
        font-size: 2.35rem;
        line-height: 1.1;
        margin-bottom: 0.35rem;
        font-weight: 650;
        color: #20242a;
    }
    .hero p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }
    .note {
        color: #64748b;
        font-size: 0.82rem;
        text-align: center;
        margin-top: 1rem;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 1rem 1.1rem;
        min-height: 112px;
    }
    div[data-testid="stMetricLabel"] {
        color: #20242a;
        font-weight: 650;
    }
    div[data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 700;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        min-height: 104px;
    }
    .metric-card .metric-label {
        color: #20242a;
        font-size: 0.95rem;
        font-weight: 650;
        margin-bottom: 0.45rem;
    }
    .metric-card .metric-value {
        color: #111827;
        font-size: 2rem;
        line-height: 1.15;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .metric-card .metric-detail {
        color: #64748b;
        font-size: 0.84rem;
    }
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 0.4rem;
    }
    .stDataFrame {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
    }
    .legend-card {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-top: 0.8rem;
        max-height: 318px;
        overflow-y: auto;
    }
    .legend-card h3 {
        font-size: 0.95rem;
        margin: 0 0 0.55rem 0;
        color: #20242a;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin: 0.22rem 0;
        color: #334155;
        font-size: 0.86rem;
    }
    .legend-dot {
        width: 0.72rem;
        height: 0.72rem;
        border-radius: 999px;
        display: inline-block;
        flex: 0 0 auto;
    }
    .section-label {
        color: #64748b;
        font-size: 0.86rem;
        margin: -0.25rem 0 0.75rem 0;
    }
    .dashboard-note {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        color: #475569;
        font-size: 0.86rem;
        line-height: 1.4;
        padding: 0.9rem 1rem;
        margin-top: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


def build_scatter(
    data: pd.DataFrame,
    y: str,
    title: str,
    y_label: str,
) -> px.scatter:
    fig = px.scatter(
        data,
        x="mred",
        y=y,
        color="variant",
        color_discrete_map=VARIANT_COLORS,
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
        title=title,
    )
    fig.update_layout(
        height=335,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=48, b=10),
        showlegend=False,
        legend_title_text="Variant",
        font=dict(color="#20242a", family="Segoe UI"),
        title=dict(font=dict(size=16)),
    )
    fig.update_xaxes(
        title="Error (MRED)",
        gridcolor="#e5e7eb",
        zeroline=False,
    )
    fig.update_yaxes(
        title=y_label,
        gridcolor="#e5e7eb",
        zeroline=False,
    )
    return fig


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


def render_variant_legend(variants: list[str]) -> None:
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
        <div class="legend-card">
          <h3>Variant colors</h3>
          {items}
        </div>
        """,
        unsafe_allow_html=True,
    )


if not DATASET_PATH.exists():
    st.error(
        "Dataset not found. Run: python src/data_generation/generate_synthetic_data.py"
    )
    st.stop()


df = load_data()

st.markdown(
    """
    <div class="hero">
      <h1>Approximate Computing Trade-off Explorer</h1>
      <p>Synthetic M-AxPPA dataset | Error, energy and area analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Filters")

    all_variants = sorted(df["variant"].unique())
    default_variants = [
        variant for variant in DEFAULT_VARIANTS if variant in all_variants
    ]

    families = st.multiselect(
        "Family",
        sorted(df["family"].unique()),
        default=sorted(df["family"].unique()),
    )

    variant_mode = st.radio(
        "Variant selection",
        ["Focused", "All", "Custom"],
        horizontal=True,
        help="Focused keeps the main M-AxPPA variants plus key baselines.",
    )

    if variant_mode == "Focused":
        variants = default_variants
        st.caption("Focused view: M-AxPPA variants and key baselines.")
    elif variant_mode == "All":
        variants = all_variants
    else:
        variants = st.multiselect(
            "Choose variants",
            all_variants,
            default=default_variants,
        )

    max_mred = st.slider(
        "Maximum MRED",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.01,
    )
    min_energy = st.slider(
        "Minimum energy savings (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0,
    )
    min_area = st.slider(
        "Minimum area savings (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0,
    )

filtered = df[
    df["family"].isin(families)
    & df["variant"].isin(variants)
    & (df["mred"] <= max_mred)
    & (df["energy_saving_pct"] >= min_energy)
    & (df["area_saving_pct"] >= min_area)
].copy()

if filtered.empty:
    st.warning("No architectures match the selected filters.")
    st.stop()

overview_tab, ranking_tab, pareto_tab, data_tab = st.tabs(
    ["Dashboard", "Rankings", "Pareto", "Data"]
)

with overview_tab:
    st.markdown(
        '<p class="section-label">Each point represents one architecture. The best region is upper-left: lower error and higher savings.</p>',
        unsafe_allow_html=True,
    )
    chart_col, side_col = st.columns([2.15, 1], gap="large")

    with chart_col:
        st.plotly_chart(
            build_scatter(
                filtered,
                "energy_saving_pct",
                "Energy Savings vs Error",
                "Energy savings (%)",
            ),
            use_container_width=True,
        )

        st.plotly_chart(
            build_scatter(
                filtered,
                "area_saving_pct",
                "Area Savings vs Error",
                "Area savings (%)",
            ),
            use_container_width=True,
        )

    with side_col:
        render_metric_card(
            "Displayed Architectures",
            f"{len(filtered):,.0f}",
            "Architectures after current filters",
        )
        render_metric_card(
            "Maximum Energy Savings",
            f"{filtered['energy_saving_pct'].max():.2f}%",
            f"Within MRED <= {max_mred:.2f}",
        )
        render_metric_card(
            "Maximum Area Savings",
            f"{filtered['area_saving_pct'].max():.2f}%",
            f"Within MRED <= {max_mred:.2f}",
        )
        render_metric_card(
            "Lowest Error",
            f"{filtered['mred'].min():.4f}",
            "Minimum MRED in the selected set",
        )
        render_variant_legend(variants)
        st.markdown(
            """
            <div class="dashboard-note">
            <strong>Decision rule:</strong><br>
            filter by acceptable error first, then rank candidates by energy,
            area, or balanced score.
            </div>
            """,
            unsafe_allow_html=True,
        )

with ranking_tab:
    ranking_metric = st.radio(
        "Ranking criterion",
        ["balanced_score", "energy_saving_pct", "area_saving_pct", "mred"],
        horizontal=True,
    )
    ascending = ranking_metric == "mred"
    top = filtered.sort_values(ranking_metric, ascending=ascending).head(15).copy()
    top["label"] = top.apply(
        lambda row: f"{row['variant']} | M={row['m_bits']}, L={row['l_bits']}, K={row['k_bits']}"
        if row["family"] == "M-AxPPA"
        else f"{row['variant']} | K={row['k_bits']}",
        axis=1,
    )

    fig_rank = px.bar(
        top,
        x=ranking_metric,
        y="label",
        color="variant",
        color_discrete_map=VARIANT_COLORS,
        orientation="h",
        title=f"Top architectures by {ranking_metric}",
    )
    fig_rank.update_layout(
        height=540,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=52, b=10),
        yaxis={"categoryorder": "total ascending"},
        font=dict(color="#20242a", family="Segoe UI"),
    )
    fig_rank.update_xaxes(gridcolor="#e5e7eb")
    fig_rank.update_yaxes(title="")
    st.plotly_chart(fig_rank, use_container_width=True)

with pareto_tab:
    pareto = filtered[
        (filtered["pareto_optimal_energy_error"] == 1)
        | (filtered["pareto_optimal_area_error"] == 1)
    ]
    fig_pareto = build_scatter(
        filtered,
        "energy_saving_pct",
        "Pareto Candidates: Energy Savings vs Error",
        "Energy savings (%)",
    )
    fig_pareto.update_traces(opacity=0.45)
    fig_pareto.add_scatter(
        x=pareto["mred"],
        y=pareto["energy_saving_pct"],
        mode="markers",
        marker={"size": 11, "symbol": "diamond", "color": "#111827"},
        name="Pareto candidate",
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

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
    <p class="note">
    Synthetic data based on the public M-AxPPA paper structure. Values demonstrate
    the analysis workflow and do not represent real hardware measurements.
    </p>
    """,
    unsafe_allow_html=True,
)
