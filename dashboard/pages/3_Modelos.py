import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.styles import CSS
from dashboard import NIGHT_BLUE

st.markdown(CSS, unsafe_allow_html=True)

reports_dir = Path("outputs/reports")
reports = sorted(reports_dir.glob("reporte_*.json"))

if not reports:
    st.markdown("""
    <div class="card">
        <h3>🤖 Comparación de Modelos</h3>
        <p>No existen reportes aún.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

latest = reports[-1]

with open(latest, encoding="utf-8") as f:
    report = json.load(f)

st.markdown("""
<div class="header-section">
    <h1>🤖 Comparación de Modelos</h1>
    <p>Rendimiento de clasificadores en la fase actual</p>
</div>
""", unsafe_allow_html=True)

summary = report.get("validation_summary", {})

data = []
for model, metrics in summary.items():
    if model == "score_model":
        continue
    data.append({
        "Modelo": model.replace("_", " ").title(),
        "Accuracy": metrics.get("accuracy", 0),
        "Precision": metrics.get("precision", 0),
        "Recall": metrics.get("recall", 0),
        "F1": metrics.get("f1", 0)
    })

df = pd.DataFrame(data)

if df.empty:
    st.markdown("""
    <div class="card">
        <h3>📊 Métricas por modelo</h3>
        <p>No hay métricas de validación disponibles para esta fase.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='card'><h3>📊 Métricas por modelo</h3></div>", unsafe_allow_html=True)

st.dataframe(
    df.style.format({
        "Accuracy": "{:.3f}",
        "Precision": "{:.3f}",
        "Recall": "{:.3f}",
        "F1": "{:.3f}"
    }),
    width='stretch',
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df, x="Modelo", y="Accuracy",
        text="Accuracy", color="Modelo",
        color_discrete_sequence=["#2C5F8A", "#00A896", "#E67E22"],
        title="Accuracy por modelo"
    )
    fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=20, l=20, r=20))
    fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

with col2:
    fig = px.bar(
        df, x="Modelo", y="F1",
        text="F1", color="Modelo",
        color_discrete_sequence=["#2C5F8A", "#00A896", "#E67E22"],
        title="F1-Score por modelo"
    )
    fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=20, l=20, r=20))
    fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
    fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
    st.plotly_chart(fig, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'><h3>🕸️ Comparación multidimensional</h3></div>", unsafe_allow_html=True)
    fig = go.Figure()
    colors = {"Logistic Regression": "#2C5F8A", "Random Forest": "#00A896", "Xgboost": "#E67E22"}
    for _, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["Accuracy"], row["Precision"], row["Recall"], row["F1"], row["Accuracy"]],
            theta=["Accuracy", "Precision", "Recall", "F1", "Accuracy"],
            fill="toself",
            name=row["Modelo"],
            line_color=colors.get(row["Modelo"], "#2C5F8A")
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickformat=".0%", gridcolor="#B0B8C4")),
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=20, r=20), title="Comparación multidimensional"
    )
    st.plotly_chart(fig, width='stretch')

with col2:
    st.markdown("<div class='card'><h3>📊 Heatmap de rendimiento</h3></div>", unsafe_allow_html=True)
    heat_df = df.set_index("Modelo")[["Accuracy", "Precision", "Recall", "F1"]]
    fig = px.imshow(
        heat_df, text_auto=".2%", aspect="auto",
        color_continuous_scale="Blues",
        title="Heatmap de métricas por modelo"
    )
    fig.update_traces(textfont=dict(color=NIGHT_BLUE))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=20, l=20, r=20), coloraxis=dict(colorbar=dict(tickfont=dict(color=NIGHT_BLUE), title=dict(font=dict(color=NIGHT_BLUE)))))
    st.plotly_chart(fig, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div class='card'><h3>📊 Comparación de todas las métricas</h3></div>", unsafe_allow_html=True)
df_melted = df.melt(id_vars=["Modelo"], value_vars=["Accuracy", "Precision", "Recall", "F1"], var_name="Métrica", value_name="Valor")
fig = px.bar(
    df_melted, x="Modelo", y="Valor", color="Métrica", barmode="group",
    text="Valor", color_discrete_map={"Accuracy": "#2C5F8A", "Precision": "#00A896", "Recall": "#E67E22", "F1": "#8E44AD"},
    title=""
)
fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", textfont=dict(color=NIGHT_BLUE))
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color=NIGHT_BLUE, family="Inter, sans-serif"), hoverlabel=dict(font=dict(color=NIGHT_BLUE)), paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=NIGHT_BLUE)))
fig.update_yaxes(tickformat=".0%", gridcolor="#B0B8C4", gridwidth=0.5); fig.update_yaxes(tickfont=dict(color=NIGHT_BLUE))
fig.update_xaxes(gridcolor="#B0B8C4", gridwidth=0.5); fig.update_xaxes(tickfont=dict(color=NIGHT_BLUE))
st.plotly_chart(fig, width='stretch')

best = report.get("best_classifier", "-")
st.markdown(f"""
<div class="card" style="text-align:center;">
    <h3>🏆 Mejor modelo</h3>
    <p style="font-size:1.3rem; font-weight:600; color:{NIGHT_BLUE};">{best}</p>
</div>
""", unsafe_allow_html=True)