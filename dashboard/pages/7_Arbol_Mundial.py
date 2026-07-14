import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.styles import CSS
from dashboard.flags import flag

st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="header-section">
    <h1>🌍 Árbol del Mundial 2026</h1>
    <p>Recorrido completo del torneo fase por fase</p>
</div>
""", unsafe_allow_html=True)

reports_dir = Path("outputs/reports")
reports = sorted(reports_dir.glob("reporte_*.json"))

if not reports:
    st.markdown("""
    <div class="card">
        <h3>🌍 Árbol del Mundial</h3>
        <p>No existen reportes aún.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

for report_file in reports:
    with open(report_file, encoding="utf-8") as f:
        data = json.load(f)

    stage = data.get("stage", "?")
    matches = data.get("matches", [])

    color_map = {
        "R32": "#2C5F8A",
        "R16": "#00A896",
        "QF": "#E67E22",
        "SF": "#8E44AD",
        "F": "#C0392B"
    }
    color = color_map.get(stage, "#2C5F8A")

    st.markdown(f"""
    <div style="background:{color}; border-radius:10px; padding:0.8rem 1.5rem; margin:1rem 0;">
        <h3 style="color:white; margin:0;">🏆 {stage}</h3>
    </div>
    """, unsafe_allow_html=True)

    for match in matches:
        team_a = match.get("team_a", "?")
        team_b = match.get("team_b", "?")
        score = match.get("predicted_score_90", {})
        winner = match.get("actual_result", {}).get("winner") or match.get("predicted_winner", "-")

        st.markdown("""
        <div class="card" style="padding:1rem 1.5rem;">
        """, unsafe_allow_html=True)

        cols = st.columns([2, 1, 2, 1])
        cols[0].markdown(f"{flag(team_a)} **{team_a}**")
        cols[1].markdown(f"`{score.get('a','-')} - {score.get('b','-')}`", help="Marcador predicho")
        cols[2].markdown(f"{flag(team_b)} **{team_b}**")

        if match.get("actual_result", {}).get("winner"):
            cols[3].success(f"✅ {winner}")
        else:
            cols[3].info(f"🔮 {winner}")

        st.markdown("</div>", unsafe_allow_html=True)