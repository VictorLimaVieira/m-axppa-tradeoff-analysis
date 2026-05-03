from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "tradeoff_dataset.csv"


st.set_page_config(
    page_title="M-AxPPA Trade-off Explorer",
    page_icon="",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


st.title("Explorador de Trade-offs em Computacao Aproximada")

if not DATASET_PATH.exists():
    st.error(
        "Dataset nao encontrado. Execute: python src/data_generation/generate_synthetic_data.py"
    )
    st.stop()

df = load_data()

st.caption(
    "MVP com dados sinteticos baseados na estrutura publica do artigo M-AxPPA. "
    "Os valores nao representam medicoes reais de hardware."
)

with st.sidebar:
    st.header("Filtros")
    families = st.multiselect(
        "Familia",
        sorted(df["family"].unique()),
        default=sorted(df["family"].unique()),
    )
    variants = st.multiselect(
        "Variante",
        sorted(df["variant"].unique()),
        default=sorted(df["variant"].unique()),
    )
    max_mred = st.slider(
        "MRED maximo",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.01,
    )
    min_energy = st.slider(
        "Economia minima de energia (%)",
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
].copy()

metric_cols = st.columns(4)
metric_cols[0].metric("Arquiteturas filtradas", len(filtered))
metric_cols[1].metric("Maior economia de energia", f"{filtered['energy_saving_pct'].max():.2f}%")
metric_cols[2].metric("Maior economia de area", f"{filtered['area_saving_pct'].max():.2f}%")
metric_cols[3].metric("Menor MRED", f"{filtered['mred'].min():.4f}")

tab_overview, tab_pareto, tab_table = st.tabs(
    ["Visao geral", "Pareto", "Tabela"]
)

with tab_overview:
    left, right = st.columns(2)

    with left:
        fig_energy = px.scatter(
            filtered,
            x="mred",
            y="energy_saving_pct",
            color="variant",
            hover_data=["family", "m_bits", "l_bits", "k_bits", "balanced_score"],
            title="Economia de energia vs erro",
        )
        st.plotly_chart(fig_energy, use_container_width=True)

    with right:
        fig_area = px.scatter(
            filtered,
            x="mred",
            y="area_saving_pct",
            color="variant",
            hover_data=["family", "m_bits", "l_bits", "k_bits", "balanced_score"],
            title="Economia de area vs erro",
        )
        st.plotly_chart(fig_area, use_container_width=True)

    top = (
        filtered.sort_values("balanced_score", ascending=False)
        .head(15)
        .assign(label=lambda data: data["variant"] + " K=" + data["k_bits"].astype(str))
    )
    fig_rank = px.bar(
        top,
        x="balanced_score",
        y="label",
        color="variant",
        orientation="h",
        title="Top arquiteturas por score balanceado",
    )
    fig_rank.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_rank, use_container_width=True)

with tab_pareto:
    pareto = filtered[
        (filtered["pareto_optimal_energy_error"] == 1)
        | (filtered["pareto_optimal_area_error"] == 1)
    ]
    fig_pareto = px.scatter(
        filtered,
        x="mred",
        y="energy_saving_pct",
        color="variant",
        opacity=0.35,
        title="Candidatas de Pareto: erro vs energia",
    )
    fig_pareto.add_scatter(
        x=pareto["mred"],
        y=pareto["energy_saving_pct"],
        mode="markers",
        marker={"size": 12, "symbol": "diamond", "color": "black"},
        name="Pareto",
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

with tab_table:
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

