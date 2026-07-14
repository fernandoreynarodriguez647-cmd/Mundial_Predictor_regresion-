import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.styles import CSS
from dashboard import NIGHT_BLUE

st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="header-section">
    <h1>📈 Métricas del Modelo</h1>
    <p>Evolución del rendimiento a través de las fases</p>
</div>
""", unsafe_allow_html=True)

metrics_file = Path("outputs/history/metrics_history.csv")

if not metrics_file.exists():
    st.markdown("""
    <div class="card">
        <h3>📈 Métricas</h3>
        <p>No existe el archivo de historial de métricas.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.read_csv(metrics_file)

required_cols = {"date", "stage", "model", "accuracy", "f1", "mae_score", "rmse_score"}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"Faltan columnas requeridas: {', '.join(missing)}")
    st.stop()

df["date"] = pd.to_datetime(df["date"])

st.markdown(f"""
<div class="card" style="text-align:center;">
    <span style="color:{NIGHT_BLUE}; font-size:0.85rem; font-weight:600;">REGISTROS CARGADOS</span>
    <p style="font-size:2rem; font-weight:700; color:{NIGHT_BLUE}; margin:0;">{len(df)}</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔍 Filtros")
    stages = st.multiselect(
        "Fase", options=df["stage"].unique(),
        default=list(df["stage"].unique())
    )
    modelos = st.multiselect(
        "Modelo", options=df["model"].unique(),
        default=list(df["model"].unique())
    )

filtered = df[df["stage"].isin(stages) & df["model"].isin(modelos)]

if filtered.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Accuracy máximo", f"{filtered['accuracy'].max()*100:.1f}%")
with col2:
    st.metric("Mejor F1", f"{filtered['f1'].max()*100:.1f}%")
with col3:
    st.metric("MAE mínimo", f"{filtered['mae_score'].min():.3f}")
with col4:
    st.metric("RMSE mínimo", f"{filtered['rmse_score'].min():.3f}")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        filtered, x="stage", y="accuracy",
        color="model", markers=True,
        color_discrete_map={
            "logistic_regression": "#2C5F8A",
            "random_forest": "#00A896",
            "xgboost": "#E67E22"
        },
        title="Accuracy por fase"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=20, r=20),
        yaxis_title="Accuracy",
        xaxis_title="Fase"
    )
    fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

with col2:
    fig = px.line(
        filtered, x="stage", y="f1",
        color="model", markers=True,
        color_discrete_map={
            "logistic_regression": "#2C5F8A",
            "random_forest": "#00A896",
            "xgboost": "#E67E22"
        },
        title="F1-Score por fase"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=20, r=20),
        yaxis_title="F1",
        xaxis_title="Fase"
    )
    fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.area(
        filtered, x="stage", y="mae_score",
        color="model", markers=True,
        color_discrete_map={
            "logistic_regression": "#2C5F8A",
            "random_forest": "#00A896",
            "xgboost": "#E67E22"
        },
        title="MAE (Error Absoluto Medio) por fase"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=20, l=20, r=20), yaxis_title="MAE", xaxis_title="Fase")
    fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

with col2:
    fig = px.area(
        filtered, x="stage", y="rmse_score",
        color="model", markers=True,
        color_discrete_map={
            "logistic_regression": "#2C5F8A",
            "random_forest": "#00A896",
            "xgboost": "#E67E22"
        },
        title="RMSE (Raíz del Error Cuadrático Medio) por fase"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=20, l=20, r=20), yaxis_title="RMSE", xaxis_title="Fase")
    fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(
        filtered, x="accuracy", y="f1", color="model", size="mae_score",
        color_discrete_map={
            "logistic_regression": "#2C5F8A",
            "random_forest": "#00A896",
            "xgboost": "#E67E22"
        },
        title="Accuracy vs F1-Score"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=20, l=20, r=20), xaxis_title="Accuracy", yaxis_title="F1")
    fig.update_xaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

with col2:
    fig = px.scatter(
        filtered, x="mae_score", y="rmse_score", color="model", size="accuracy",
        color_discrete_map={
            "logistic_regression": "#2C5F8A",
            "random_forest": "#00A896",
            "xgboost": "#E67E22"
        },
        title="MAE vs RMSE"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=20, l=20, r=20), xaxis_title="MAE", yaxis_title="RMSE")
    fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

st.markdown("<br><div class='card'><h3>📋 Historial completo</h3></div>", unsafe_allow_html=True)

display = filtered.copy()
display["accuracy"] = (display["accuracy"] * 100).round(1).astype(str) + "%"
display["f1"] = (display["f1"] * 100).round(1).astype(str) + "%"

st.dataframe(display, width='stretch', hide_index=True)