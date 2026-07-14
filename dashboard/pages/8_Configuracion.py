import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from dashboard.styles import CSS

st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="header-section">
    <h1>⚙️ Configuración del Sistema</h1>
    <p>Estado y verificación de componentes</p>
</div>
""", unsafe_allow_html=True)

now = datetime.now()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estado", "Operativo", delta="Online")
with col2:
    st.metric("Hora", now.strftime("%H:%M"))
with col3:
    st.metric("Fecha", now.strftime("%d/%m/%Y"))

st.markdown("<br><div class='card'><h3>📁 Directorios del proyecto</h3></div>", unsafe_allow_html=True)

paths = {
    "Reportes": "outputs/reports",
    "Historial": "outputs/history",
    "Modelos": "saved_models",
    "Datos": "data",
    "Logs": "outputs/logs"
}

cols = st.columns(len(paths))
for i, (name, path) in enumerate(paths.items()):
    folder = Path(path)
    with cols[i]:
        if folder.exists():
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">{name}</div>
                <div class="value accent">✔</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">{name}</div>
                <div class="value warning">✖</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><div class='card'><h3>📄 Reportes generados</h3></div>", unsafe_allow_html=True)

reports = list(Path("outputs/reports").glob("*.json"))
if reports:
    for r in reports:
        st.markdown(f"""
        <div style="background:#F0F2F5; border-radius:6px; padding:0.3rem 0.8rem; margin:0.2rem 0; font-size:0.9rem;">
            📄 {r.name}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<p>No hay reportes generados.</p>', unsafe_allow_html=True)

st.markdown("<br><div class='card'><h3>🤖 Modelos ML</h3></div>", unsafe_allow_html=True)
modelos = ["Logistic Regression", "Random Forest", "XGBoost"]
cols = st.columns(len(modelos))
for i, m in enumerate(modelos):
    with cols[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Modelo</div>
            <div class="value" style="font-size:1.2rem;">{m}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<br><div class="card">
    <h3>📌 Información</h3>
    <p style="font-size:0.9rem;">
        Este dashboard se actualiza automáticamente al ejecutar el pipeline.
        Solo es necesario actualizar los resultados oficiales y ejecutar nuevamente
        <code>scripts/run_stage.py</code> y <code>scripts/update_stage.py</code> para cada fase.
    </p>
</div>
""", unsafe_allow_html=True)