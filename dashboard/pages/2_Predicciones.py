from pathlib import Path
import json
import streamlit as st
import pandas as pd

st.title("⚽ Predicciones del Mundial")

reports_dir = Path("outputs/reports")
reports = sorted(reports_dir.glob("reporte_*.json"))

if not reports:
    st.warning("No existen reportes.")
    st.stop()

latest = reports[-1]

with open(latest, encoding="utf-8") as f:
    report = json.load(f)

stage = report.get("stage", "-")

st.success(f"Fase actual: {stage}")

rows = []

for match in report.get("matches", []):

    score = match.get("predicted_score_90", {})

    fila = {
        "Partido": f'{match.get("team_a","?")} vs {match.get("team_b","?")}',
        "Marcador Predicho": f'{score.get("a","-")}-{score.get("b","-")}',
        "Ganador Predicho": match.get("predicted_winner","-"),
        "Probabilidad": f'{match.get("advance_probability_avg_a",0)*100:.1f}%'
    }

    if "actual_result" in match:

        actual = match["actual_result"]["score_90"]

        fila["Resultado Real"] = f'{actual["a"]}-{actual["b"]}'

        fila["Estado"] = (
            "✅ Acierto"
            if match.get("hit", False)
            else "❌ Fallo"
        )

    rows.append(fila)

df = pd.DataFrame(rows)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    df.set_index("Partido")["Probabilidad"].str.replace("%", "").astype(float)
)