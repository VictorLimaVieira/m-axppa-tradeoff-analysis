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
        color_discrete_sequence=COLOR_SEQUENCE,
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
        height=390,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=52, b=10),
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

    families = st.multiselect(
        "Family",
        sorted(df["family"].unique()),
        default=sorted(df["family"].unique()),
    )
    variants = st.multiselect(
        "Variant",
        sorted(df["variant"].unique()),
        default=sorted(df["variant"].unique()),
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

metric_cols = st.columns(4)
metric_cols[0].metric("Displayed Architectures", f"{len(filtered):,.0f}")
metric_cols[1].metric(
    "Maximum Energy Savings",
    f"{filtered['energy_saving_pct'].max():.2f}%",
)
metric_cols[2].metric(
    "Maximum Area Savings",
    f"{filtered['area_saving_pct'].max():.2f}%",
)
metric_cols[3].metric("Lowest MRED", f"{filtered['mred'].min():.4f}")

overview_tab, ranking_tab, pareto_tab, data_tab = st.tabs(
    ["Overview", "Rankings", "Pareto", "Data"]
)

with overview_tab:
    left, right = st.columns(2)

    with left:
        st.plotly_chart(
            build_scatter(
                filtered,
                "energy_saving_pct",
                "Energy Savings vs Error",
                "Energy savings (%)",
            ),
            use_container_width=True,
        )

    with right:
        st.plotly_chart(
            build_scatter(
                filtered,
                "area_saving_pct",
                "Area Savings vs Error",
                "Area savings (%)",
            ),
            use_container_width=True,
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
        color_discrete_sequence=COLOR_SEQUENCE,
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

