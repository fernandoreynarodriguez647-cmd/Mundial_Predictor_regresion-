import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.styles import CSS

from dashboard import NIGHT_BLUE

st.markdown(CSS, unsafe_allow_html=True)

reports_dir = Path("outputs/reports")
reports = sorted(reports_dir.glob("reporte_*.json"))

if not reports:
    st.markdown("""
    <div class="card">
        <h3>⚽ Predicciones</h3>
        <p>No existen reportes aún.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

latest = reports[-1]

with open(latest, encoding="utf-8") as f:
    report = json.load(f)

stage = report.get("stage", "-")

st.markdown(f"""
<div class="header-section">
    <h1>⚽ Predicciones - Fase {stage}</h1>
    <p>Partidos predichos con modelos de Machine Learning</p>
</div>
""", unsafe_allow_html=True)

rows = []
for match in report.get("matches", []):
    score = match.get("predicted_score_90", {})
    prob_a = match.get("advance_probability_avg_a", 0)
    prob_b = round(1 - prob_a, 4)
    ta = match.get("team_a","?")
    tb = match.get("team_b","?")
    fila = {
        "Partido": f'{ta} vs {tb}',
        "Marcador": f'{score.get("a","-")} - {score.get("b","-")}',
        "Ganador": match.get("predicted_winner", "-"),
        "Prob. A": f"{prob_a:.1%}",
        "Prob. B": f"{prob_b:.1%}",
    }
    if "actual_result" in match:
        actual = match["actual_result"].get("score_90", {})
        fila["Resultado Real"] = f'{actual.get("a","-")} - {actual.get("b","-")}'
        fila["Estado"] = "✅ Acierto" if match.get("hit", False) else "❌ Fallo"
    rows.append(fila)

df = pd.DataFrame(rows)

if not df.empty:
    st.dataframe(df, width='stretch', hide_index=True)
else:
    st.markdown("""
    <div class="card">
        <p>No hay partidos disponibles en este reporte.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'><h3>📊 Probabilidades de avance</h3></div>", unsafe_allow_html=True)
    prob_rows = []
    for m in report.get("matches", []):
        ta = m.get("team_a", "?")
        tb = m.get("team_b", "?")
        prob_a = m.get("advance_probability_avg_a", 0)
        prob_rows.append({"Equipo": f"{ta}", "Probabilidad": prob_a, "Tipo": "Local"})
        prob_rows.append({"Equipo": f"{tb}", "Probabilidad": round(1 - prob_a, 4), "Tipo": "Visita"})
    if prob_rows:
        df_probs = pd.DataFrame(prob_rows)
        fig = px.bar(
            df_probs, y="Equipo", x="Probabilidad", color="Tipo", orientation="h",
            barmode="group", text="Probabilidad",
            color_discrete_map={"Local": "#2C5F8A", "Visita": "#E67E22"},
            title="Probabilidades de avance por equipo"
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), xaxis_title="Probabilidad", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=NIGHT_BLUE)))
        fig.update_xaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
        fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
        st.plotly_chart(fig, width='stretch')

with col2:
    st.markdown("<div class='card'><h3>📊 Marcadores predichos</h3></div>", unsafe_allow_html=True)
    score_rows = []
    for m in report.get("matches", []):
        score = m.get("predicted_score_90", {})
        ta = m.get("team_a", "?")
        tb = m.get("team_b", "?")
        score_rows.append({"Equipo": f"{ta}", "Goles": score.get("a", 0), "Partido": f"{ta} vs {tb}"})
        score_rows.append({"Equipo": f"{tb}", "Goles": score.get("b", 0), "Partido": f"{ta} vs {tb}"})
    if score_rows:
        df_scores = pd.DataFrame(score_rows)
        fig = px.scatter(
            df_scores, x="Equipo", y="Goles", size="Goles", color="Goles",
            color_continuous_scale="Blues", size_max=30,
            title="Distribución de goles predichos"
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), coloraxis=dict(colorbar=dict(tickfont=dict(color=NIGHT_BLUE), title=dict(font=dict(color=NIGHT_BLUE)))))
        fig.update_yaxes(dtick=1, gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
        fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
        st.plotly_chart(fig, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='card'><h3>📊 Matriz de probabilidades de marcadores</h3></div>", unsafe_allow_html=True)

from scipy.stats import poisson

matches = report.get("matches", [])
match_ids = [f"{m['match_id']} - {m['team_a']} vs {m['team_b']}" for m in matches]
if match_ids:
    selected = st.selectbox("Seleccionar partido", match_ids)
    idx = match_ids.index(selected)
    match = matches[idx]
    lam_a = match["predicted_score_90"]["a"]
    lam_b = match["predicted_score_90"]["b"]
    max_goals = 5
    scores = list(range(max_goals + 1))
    probs = [[poisson.pmf(i, lam_a) * poisson.pmf(j, lam_b) for j in scores] for i in scores]
    prob_matrix = pd.DataFrame(probs, index=[str(s) for s in scores], columns=[str(s) for s in scores])
    prob_matrix.index.name = "Team A"
    prob_matrix.columns = [f"Team B: {s}" for s in scores]
    fig = px.imshow(
        prob_matrix,
        text_auto=".1%",
        aspect="auto",
        color_continuous_scale="Blues",
        title=f"Probabilidad de resultado: {match['team_a']} vs {match['team_b']} (λ={lam_a}-{lam_b})",
    )
    fig.update_traces(textfont=dict(color=NIGHT_BLUE))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"),
        hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis_title="Goles Equipo B",
        yaxis_title="Goles Equipo A",
        coloraxis=dict(colorbar=dict(tickfont=dict(color=NIGHT_BLUE), title=dict(font=dict(color=NIGHT_BLUE)))),
    )
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

    st.markdown(f"""
    <div style="text-align:center; font-size:0.9rem; color:{NIGHT_BLUE};">
        📌 <b>{match['team_a']}</b> promedio {lam_a} goles | <b>{match['team_b']}</b> promedio {lam_b} goles
        — basado en distribución Poisson
    </div>
    """, unsafe_allow_html=True)
