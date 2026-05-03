from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"

VARIANT_COLORS = {
    "AxPPA": "#2563EB",
    "COPY": "#1E3A8A",
    "HOERAA": "#EA580C",
    "LDCA": "#86198F",
    "LOA": "#DB2777",
    "LZTA": "#7C3AED",
    "M-AxPPA-COPY": "#D97706",
    "M-AxPPA-LOA": "#E11D48",
    "M-AxPPA-TRUNC": "#0F766E",
    "M-HEAA": "#16A34A",
    "TRUNC": "#0891B2",
}


st.set_page_config(
    page_title="M-AxPPA Trade-off Explorer",
    page_icon="",
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
        max-width: 1240px;
        padding-top: 1.45rem;
        padding-bottom: 2rem;
    }

    .hero {
        text-align: center;
        margin-bottom: 1.1rem;
    }

    .hero h1 {
        color: #1f2937;
        font-size: 2.2rem;
        font-weight: 650;
        line-height: 1.1;
        margin: 0 0 0.45rem 0;
    }

    .hero p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.75rem;
    }

    .metric-label {
        color: #1f2937;
        font-size: 0.9rem;
        font-weight: 650;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #111827;
        font-size: 1.8rem;
        font-weight: 720;
        line-height: 1.15;
    }

    .metric-detail {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 0.15rem;
    }

    .chart-title {
        color: #1f2937;
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 0.15rem 0;
    }

    .chart-subtitle {
        color: #64748b;
        font-size: 0.82rem;
        margin: 0 0 0.55rem 0;
    }

    .legend-panel {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-top: 0.75rem;
    }

    .legend-panel h3 {
        color: #1f2937;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.55rem 0;
    }

    .legend-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.28rem;
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

    .decision-note {
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        color: #475569;
        font-size: 0.84rem;
        line-height: 1.42;
        margin-top: 0.75rem;
        padding: 0.85rem 1rem;
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

    label, p, span {
        color: inherit;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


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
        <div class="legend-panel">
          <h3>Variant colors</h3>
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
) -> px.scatter:
    max_x = max(0.30, float(data["mred"].max()) * 1.08)
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
        height=292,
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
        range=[0, max_x],
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

chart_col, side_col = st.columns([2.1, 1], gap="large")

with side_col:
    metric_slot = st.container()

    with st.container(border=True):
        selected_variants = st.multiselect(
            "Variant",
            all_variants,
            default=all_variants,
            help="Select the architecture variants shown in the charts.",
        )

    with st.container(border=True):
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

if not selected_variants:
    selected_variants = all_variants

filtered = df[
    df["variant"].isin(selected_variants)
    & (df["mred"] <= max_mred)
    & (df["energy_saving_pct"] >= min_energy)
    & (df["area_saving_pct"] >= min_area)
].copy()

with metric_slot:
    if filtered.empty:
        render_metric_card("Displayed Architectures", "0", "No rows match filters")
        render_metric_card("Maximum Energy Savings", "-", "Adjust filters")
        render_metric_card("Maximum Area Savings", "-", "Adjust filters")
    else:
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

    render_legend(selected_variants)
    st.markdown(
        """
        <div class="decision-note">
        <strong>Decision rule:</strong><br>
        filter by acceptable error first, then rank candidates by energy,
        area, or balanced score.
        </div>
        """,
        unsafe_allow_html=True,
    )

with chart_col:
    st.markdown(
        '<p style="color:#475569;font-size:0.9rem;margin:0 0 0.7rem 0;">Each point represents one architecture. The best region is upper-left: lower error and higher savings.</p>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning("No architectures match the selected filters.")
    else:
        with st.container(border=True):
            st.markdown(
                """
                <p class="chart-title">Energy Savings (%) vs Error (MRED)</p>
                <p class="chart-subtitle">Architectures with controlled error and energy-saving trade-offs.</p>
                """,
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                build_scatter(
                    filtered,
                    "energy_saving_pct",
                    "Energy savings (%)",
                    selected_variants,
                ),
                use_container_width=True,
            )

        with st.container(border=True):
            st.markdown(
                """
                <p class="chart-title">Area Savings (%) vs Error (MRED)</p>
                <p class="chart-subtitle">Architectures with controlled error and circuit-area trade-offs.</p>
                """,
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                build_scatter(
                    filtered,
                    "area_saving_pct",
                    "Area savings (%)",
                    selected_variants,
                ),
                use_container_width=True,
            )

if not filtered.empty:
    ranking_tab, pareto_tab, data_tab = st.tabs(["Rankings", "Pareto", "Data"])

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
            yaxis={"categoryorder": "total ascending"},
            font=dict(color="#1f2937", family="Segoe UI"),
        )
        fig_rank.update_xaxes(gridcolor="#dfe4ec", tickfont={"color": "#475569"})
        fig_rank.update_yaxes(title="", tickfont={"color": "#475569"})
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
