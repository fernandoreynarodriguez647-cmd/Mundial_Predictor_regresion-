import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.styles import CSS
from dashboard.flags import flag
from dashboard import NIGHT_BLUE

st.markdown(CSS, unsafe_allow_html=True)

reports_dir = Path("outputs/reports")
reports = sorted(reports_dir.glob("reporte_*.json"))

if not reports:
    st.markdown("""
    <div class="card">
        <h3>📊 Resumen General</h3>
        <p>No existen reportes aún. Ejecute el pipeline para generar predicciones.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

latest = reports[-1]

with open(latest, encoding="utf-8") as f:
    report = json.load(f)

st.markdown("""
<div class="header-section">
    <h1>📊 Resumen General</h1>
    <p>Vista general del estado actual del torneo</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Fase actual", report.get("stage", "-"))

with col2:
    st.metric("Partidos", report.get("prediction_matches", len(report.get("matches", []))))

with col3:
    acc = report.get("prediction_accuracy", 0)
    st.metric("Accuracy", f"{acc:.2%}")

with col4:
    st.metric("Aciertos", report.get("prediction_hits", 0))

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🤖 Mejor Modelo</h3>
    </div>
    """, unsafe_allow_html=True)
    st.info(report.get("best_classifier", "Ensemble"))

with col2:
    st.markdown("""
    <div class="card">
        <h3>⏭ Siguiente Fase</h3>
    </div>
    """, unsafe_allow_html=True)
    next_stage = report.get("next_stage", "-")
    if next_stage and next_stage != "-":
        st.success(f"Preparar predicción para: {next_stage}")
    else:
        st.info("Todas las fases completadas")

st.markdown("<br>", unsafe_allow_html=True)

matches = report.get("matches", [])
if matches:
    st.markdown("<div class='card'><h3>⚽ Últimos partidos</h3></div>", unsafe_allow_html=True)
    for m in matches[-5:]:
        score = m.get("predicted_score_90", {})
        team_a = m.get("team_a", "?")
        team_b = m.get("team_b", "?")
        winner = m.get("predicted_winner", "-")
        cols = st.columns([3, 1, 1])
        cols[0].markdown(f"{flag(team_a)} **{team_a}** vs {flag(team_b)} **{team_b}**")
        cols[1].markdown(f"`{score.get('a','-')}-{score.get('b','-')}`")
        cols[2].markdown(f"🏆 {winner}")

st.markdown("<br>", unsafe_allow_html=True)

metrics_file = Path("outputs/history/metrics_history.csv")
if metrics_file.exists():
    metrics_df = pd.read_csv(metrics_file)
    metrics_df = metrics_df.drop_duplicates(subset=["stage", "model"], keep="last")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'><h3>🎯 Accuracy por fase</h3></div>", unsafe_allow_html=True)
        acc_by_stage = metrics_df.groupby("stage")["accuracy"].max().reset_index()
        fig = px.bar(
            acc_by_stage, x="stage", y="accuracy",
            text="accuracy", color="accuracy",
            color_continuous_scale="Blues",
            title="Mejor accuracy por fase"
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)) , paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), coloraxis=dict(colorbar=dict(tickfont=dict(color=NIGHT_BLUE), title=dict(font=dict(color=NIGHT_BLUE)))))
        fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
        fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.markdown("<div class='card'><h3>🎯 Aciertos vs Fallos global</h3></div>", unsafe_allow_html=True)
        total_hits = sum(r.get("prediction_hits", 0) for r in [json.load(open(f, encoding="utf-8")) for f in reports])
        total_misses = sum(r.get("prediction_misses", 0) for r in [json.load(open(f, encoding="utf-8")) for f in reports])
        if total_hits + total_misses > 0:
            fig = px.pie(
                values=[total_hits, total_misses],
                names=["Aciertos", "Fallos"],
                color=["Aciertos", "Fallos"],
                color_discrete_map={"Aciertos": "#00A896", "Fallos": "#E74C3C"},
                hole=0.4,
                title="Aciertos vs Fallos (global)"
            )
            fig.update_traces(textinfo="label+percent", textposition="outside", textfont=dict(color=NIGHT_BLUE))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)) , paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig, width='stretch')

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'><h3>📈 Evolución del accuracy por modelo</h3></div>", unsafe_allow_html=True)
        fig = px.line(
            metrics_df, x="stage", y="accuracy", color="model", markers=True,
            color_discrete_map={"logreg": "#2C5F8A", "random_forest": "#00A896", "xgboost": "#E67E22"},
            title=""
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)) , paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=20, l=20, r=20))
        fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
        fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.markdown("<div class='card'><h3>📊 Distribución de predicciones SF</h3></div>", unsafe_allow_html=True)
        match_probs = []
        for m in report.get("matches", []):
            prob = m.get("advance_probability_avg_a", 0)
            match_probs.append({"Partido": f"{flag(m['team_a'])} {m['team_a']} vs {flag(m['team_b'])} {m['team_b']}", "Prob. Avance A": prob, "Prob. Avance B": 1 - prob})
        if match_probs:
            df_probs = pd.DataFrame(match_probs)
            fig = px.bar(
                df_probs, x="Partido", y=["Prob. Avance A", "Prob. Avance B"],
                barmode="group", color_discrete_map={"Prob. Avance A": "#2C5F8A", "Prob. Avance B": "#E67E22"},
                title="Probabilidades de avance"
            )
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)) , paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), yaxis_title="Probabilidad", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
            fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
            st.plotly_chart(fig, width='stretch')