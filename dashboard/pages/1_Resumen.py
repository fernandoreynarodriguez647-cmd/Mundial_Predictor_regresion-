from pathlib import Path
import json
import streamlit as st

st.title("📊 Resumen General")

reports_dir = Path("outputs/reports")

reports = sorted(reports_dir.glob("reporte_*.json"))

if not reports:
    st.warning("No existen reportes.")
    st.stop()

latest = reports[-1]

with open(latest, encoding="utf-8") as f:
    report = json.load(f)

st.success(f"Reporte cargado: {latest.name}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Fase", report.get("stage", "-"))

    st.metric(
        "Partidos",
        report.get(
            "prediction_matches",
            len(report.get("matches", []))
        )
    )

with col2:
    st.metric(
        "Accuracy",
        f"{report.get('prediction_accuracy',0):.2%}"
    )

    st.metric(
        "Aciertos",
        report.get("prediction_hits",0)
    )

st.divider()

st.subheader("Modelo")

st.info(report.get("best_classifier","Ensemble"))

st.subheader("Siguiente fase")

st.success(report.get("next_stage","-"))