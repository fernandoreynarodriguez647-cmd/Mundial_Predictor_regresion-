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
    <h1>🕒 Historial del Sistema</h1>
    <p>Todas las predicciones generadas durante el torneo</p>
</div>
""", unsafe_allow_html=True)

history_file = Path("outputs/history/predictions_history.csv")

if not history_file.exists():
    st.markdown("""
    <div class="card">
        <h3>🕒 Historial</h3>
        <p>No existe el archivo de historial de predicciones.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.read_csv(history_file)

required_cols = {"date", "stage", "team_a", "team_b", "predicted_score_a", "predicted_score_b", "probability"}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"Faltan columnas requeridas: {', '.join(missing)}")
    st.stop()

df["date"] = pd.to_datetime(df["date"])

latest = df["date"].max()
latest_data = df[df["date"] == latest]

if latest_data.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Última ejecución", latest.strftime("%d/%m %H:%M"))
with col2:
    st.metric("Fase actual", latest_data["stage"].iloc[0])
with col3:
    st.metric("Partidos procesados", len(latest_data))
with col4:
    st.metric("Total histórico", len(df))

st.markdown("<br>", unsafe_allow_html=True)

timeline = df.groupby(["date", "stage"]).size().reset_index(name="matches")
fig = px.line(
    timeline, x="date", y="matches",
    color="stage", markers=True,
    title="Partidos procesados por ejecución",
    color_discrete_sequence=["#2C5F8A", "#00A896", "#E67E22", "#8E44AD", "#C0392B"]
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=40, b=20, l=20, r=20)
)
fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
st.plotly_chart(fig, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'><h3>📊 Partidos por fase</h3></div>", unsafe_allow_html=True)
    stage_counts = df.groupby("stage").size().reset_index(name="cantidad")
    fig = px.bar(
        stage_counts, x="stage", y="cantidad", text="cantidad", color="stage",
        color_discrete_map={"R32": "#2C5F8A", "R16": "#00A896", "QF": "#E67E22", "SF": "#8E44AD", "F": "#C0392B"},
        title="Predicciones por fase"
    )
    fig.update_traces(textposition="outside", textfont=dict(color=NIGHT_BLUE))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), showlegend=False)
    fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

with col2:
    st.markdown("<div class='card'><h3>📊 Distribución de probabilidades</h3></div>", unsafe_allow_html=True)
    if "probability" in latest_data.columns:
        fig = px.histogram(
            latest_data, x="probability", nbins=10,
            color_discrete_sequence=["#2C5F8A"],
            title="Distribución de probabilidades de acierto"
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), xaxis_title="Probabilidad", yaxis_title="Frecuencia")
        fig.update_xaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
        fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
        st.plotly_chart(fig, width='stretch')

st.markdown("<br><div class='card'><h3>⚽ Últimas predicciones</h3></div>", unsafe_allow_html=True)

show = latest_data.copy()
show["partido"] = show["team_a"] + " vs " + show["team_b"]
show["prediccion"] = show["predicted_score_a"].astype(str) + " - " + show["predicted_score_b"].astype(str)
if "real_score_a" in show.columns:
    score_a = show["real_score_a"].fillna("-").astype(str)
else:
    score_a = pd.Series(["-"] * len(show), index=show.index)
if "real_score_b" in show.columns:
    score_b = show["real_score_b"].fillna("-").astype(str)
else:
    score_b = pd.Series(["-"] * len(show), index=show.index)
show["resultado_real"] = score_a + " - " + score_b
show["prob"] = (show.get("probability", 0) * 100).round(1).astype(str) + "%"

table_cols = ["partido", "prediccion", "resultado_real", "predicted_winner", "real_winner", "prob"]
available = [c for c in table_cols if c in show.columns]
table = show[available]
st.dataframe(table, width='stretch', hide_index=True)

st.markdown("<br><div class='card'><h3>🔎 Buscar historial</h3></div>", unsafe_allow_html=True)

stage_filter = st.selectbox(
    "Seleccionar fase", ["Todas"] + list(df["stage"].unique())
)

filtered = df.copy()
if stage_filter != "Todas":
    filtered = filtered[filtered["stage"] == stage_filter]

st.write(f"Registros encontrados: {len(filtered)}")
st.dataframe(filtered, width='stretch', hide_index=True)