from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"

VARIANT_COLORS = {
    "AxPPA": "#2563EB",
    "COPY": "#312E81",
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
        height: 0 !important;
    }
    .stApp {
        background: #f6f7f9;
        color: #20242a;
    }
    .block-container {
        padding-top: 1.45rem;
        padding-bottom: 2rem;
        max-width: 1230px;
    }
    .hero {
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        font-size: 2.25rem;
        line-height: 1.08;
        margin: 0 0 0.45rem 0;
        font-weight: 650;
        color: #20242a;
    }
    .hero p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 0.4rem;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
        min-height: 96px;
    }
    .metric-label {
        color: #20242a;
        font-size: 0.92rem;
        font-weight: 650;
        margin-bottom: 0.38rem;
    }
    .metric-value {
        color: #111827;
        font-size: 1.85rem;
        line-height: 1.15;
        font-weight: 720;
        margin-bottom: 0.16rem;
    }
    .metric-detail {
        color: #64748b;
        font-size: 0.82rem;
    }
    .panel {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.9rem;
    }
    .panel h3 {
        margin: 0 0 0.55rem 0;
        color: #20242a;
        font-size: 0.98rem;
        font-weight: 650;
    }
    .panel-note {
        color: #64748b;
        font-size: 0.8rem;
        margin: -0.15rem 0 0.55rem 0;
    }
    .section-label {
        color: #64748b;
        font-size: 0.86rem;
        margin: -0.2rem 0 0.72rem 0;
    }
    .footer-note {
        border-top: 1px solid #d9dee7;
        color: #64748b;
        font-size: 0.82rem;
        line-height: 1.4;
        margin-top: 1.25rem;
        padding-top: 0.8rem;
        text-align: center;
    }
    .stDataFrame {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
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


def build_scatter(
    data: pd.DataFrame,
    y: str,
    title: str,
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
    fig.update_traces(
        marker={
            "size": 8,
            "opacity": 0.9,
            "line": {"width": 0.6, "color": "#ffffff"},
        }
    )
    fig.update_layout(
        height=328,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=58, b=8),
        font=dict(color="#20242a", family="Segoe UI"),
        title=dict(font=dict(size=16, color="#20242a")),
        legend={
            "title": {"text": "Variant"},
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "font": {"size": 10, "color": "#334155"},
            "itemsizing": "constant",
        },
    )
    fig.update_xaxes(
        title="Error (MRED)",
        gridcolor="#e5e7eb",
        zeroline=False,
        range=[0, max(0.30, float(data["mred"].max()) * 1.08)],
    )
    fig.update_yaxes(
        title=y_label,
        gridcolor="#e5e7eb",
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

chart_col, side_col = st.columns([2.05, 1], gap="large")

with side_col:
    metric_slot = st.container()

    with st.container(border=True):
        st.markdown("**Variant**")
        st.caption("Select the architecture families shown in the charts.")
        selected_variants = [
            variant
            for variant in all_variants
            if st.checkbox(variant, value=True, key=f"variant_{variant}")
        ]

    with st.container(border=True):
        st.markdown("**Thresholds**")
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

with chart_col:
    st.markdown(
        '<p class="section-label">Each point represents one architecture. The best region is upper-left: lower error and higher savings.</p>',
        unsafe_allow_html=True,
    )
    if filtered.empty:
        st.warning("No architectures match the selected filters.")
    else:
        st.plotly_chart(
            build_scatter(
                filtered,
                "energy_saving_pct",
                "Energy Savings (%) vs Error (MRED)",
                "Energy savings (%)",
                selected_variants,
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            build_scatter(
                filtered,
                "area_saving_pct",
                "Area Savings (%) vs Error (MRED)",
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
            "Pareto Candidates: Energy Savings (%) vs Error (MRED)",
            "Energy savings (%)",
            selected_variants,
        )
        fig_pareto.update_traces(opacity=0.42)
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
