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
        <h3>🧠 Explicabilidad</h3>
        <p>No existen reportes aún.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

latest = reports[-1]

with open(latest, encoding="utf-8") as f:
    report = json.load(f)

st.markdown("""
<div class="header-section">
    <h1>🧠 Explicabilidad del Modelo</h1>
    <p>Factores que influyen en las predicciones</p>
</div>
""", unsafe_allow_html=True)

decision = report.get("decision_support", {})

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🎯 Modelo seleccionado</h3>
    </div>
    """, unsafe_allow_html=True)
    st.info(decision.get("selected_model", "-"))

with col2:
    st.markdown("""
    <div class="card">
        <h3>📝 Razón</h3>
    </div>
    """, unsafe_allow_html=True)
    st.info(decision.get("selection_reason", "-"))

factors = decision.get("main_factors", [])

if not factors:
    st.markdown("""
    <div class="card">
        <h3>🔍 Factores principales</h3>
        <p>No hay factores de decisión disponibles.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df_factors = pd.DataFrame(factors)

if "importance" not in df_factors.columns or "feature" not in df_factors.columns:
    st.markdown("""
    <div class="card">
        <p>Los datos de factores no tienen la estructura esperada.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df_factors = df_factors.sort_values("importance")

fig = px.bar(
    df_factors, x="importance", y="feature",
    orientation="h", text="importance",
    color="importance", color_continuous_scale="Blues",
    title="Importancia de variables"
)
fig.update_traces(texttemplate="%{text:.3f}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=40, b=20, l=20, r=20),
    xaxis_title="Importancia",
    yaxis_title="Variable",
    coloraxis_showscale=False
)
fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))

st.plotly_chart(fig, width='stretch')

st.markdown("<br><div class='card'><h3>📋 Detalle de factores</h3></div>", unsafe_allow_html=True)
st.dataframe(df_factors, width='stretch', hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

top_features = report.get("top_features", {})
if top_features:
    st.markdown("<div class='card'><h3>📊 Comparación de features entre modelos</h3></div>", unsafe_allow_html=True)
    feature_rows = []
    for model_name, features in top_features.items():
        for feat_name, feat_imp in features[:5]:
            feature_rows.append({"Modelo": model_name.replace("_", " ").title(), "Feature": feat_name, "Importancia": abs(feat_imp)})
    if feature_rows:
        df_feat = pd.DataFrame(feature_rows)
        fig = px.bar(
            df_feat, x="Importancia", y="Feature", color="Modelo", orientation="h",
            barmode="group", text="Importancia",
            color_discrete_map={"Logreg": "#2C5F8A", "Random Forest": "#00A896", "Xgboost": "#E67E22"},
            title="Top features por modelo"
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), xaxis_title="Importancia", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=NIGHT_BLUE)))
        fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
        fig.update_yaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
        st.plotly_chart(fig, width='stretch')