import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import streamlit as st
from dashboard.styles import CSS

st.set_page_config(
    page_title="Predictor Mundial 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="header-section">
    <h1>🏆 Predictor Mundial FIFA 2026</h1>
    <p>Centro de analítica y predicción basado en Machine Learning</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📊 Predicciones</h3>
        <p>
            Resultados predichos para cada fase del torneo, incluyendo marcadores y probabilidades de avance.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🤖 Modelos ML</h3>
        <p>
            Comparación de rendimiento entre Logistic Regression, Random Forest y XGBoost.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>📈 Métricas</h3>
        <p>
            Evolución de accuracy, F1-score y errores a lo largo de las fases del torneo.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
    <div class="card">
        <h3>💡 ¿Cómo funciona?</h3>
        <p>
            El pipeline avanza fase por fase utilizando únicamente resultados oficiales ya disputados.
            Los modelos se entrenan con datos históricos de los mundiales 2014, 2018 y 2022.
            Cada nueva fase requiere que la anterior haya sido validada con resultados reales.
        </p>
    <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-top:1rem;">
        <span style="background:#E8F8F5; color:#00A896; padding:0.3rem 0.8rem; border-radius:20px; font-size:0.8rem;">R32</span>
        <span style="background:#E8F8F5; color:#00A896; padding:0.3rem 0.8rem; border-radius:20px; font-size:0.8rem;">R16</span>
        <span style="background:#E8F8F5; color:#00A896; padding:0.3rem 0.8rem; border-radius:20px; font-size:0.8rem;">QF</span>
        <span style="background:#E8F8F5; color:#00A896; padding:0.3rem 0.8rem; border-radius:20px; font-size:0.8rem;">SF</span>
        <span style="background:#E8F8F5; color:#00A896; padding:0.3rem 0.8rem; border-radius:20px; font-size:0.8rem;">FINAL</span>
    </div>
</div>
""", unsafe_allow_html=True)
