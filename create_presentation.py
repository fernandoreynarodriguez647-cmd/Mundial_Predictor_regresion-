from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import json
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ─── Paleta de colores ───
GOLD = RGBColor(0xD4, 0xAF, 0x37)
DARK_BG = RGBColor(0x0D, 0x0D, 0x0D)
DARK2 = RGBColor(0x1A, 0x1A, 0x2E)
CARD_BG = RGBColor(0x16, 0x16, 0x16)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xBB, 0xBB, 0xBB)
SOFT_WHITE = RGBColor(0xF0, 0xF0, 0xF0)
GREEN_ACCENT = RGBColor(0x00, 0xA8, 0x96)
RED_ACCENT = RGBColor(0xE7, 0x4C, 0x3C)
BLUE_ACCENT = RGBColor(0x34, 0x98, 0xDB)

# ─── Funciones auxiliares ───
def add_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, color, alpha=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    if alpha is not None:
        from pptx.oxml.ns import qn
        solidFill = shape.fill._fill
        srgb = solidFill.find(qn('a:solidFill')).find(qn('a:srgbClr'))
        if srgb is not None:
            alpha_elem = srgb.makeelement(qn('a:alpha'), {'val': str(int(alpha * 1000))})
            srgb.append(alpha_elem)
    return shape

def add_textbox(slide, left, top, width, height, text, font_size=18, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_para(text_frame, text, font_size=16, color=LIGHT_GRAY, bold=False, space_before=Pt(6), alignment=PP_ALIGN.LEFT):
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = 'Calibri'
    p.space_before = space_before
    p.alignment = alignment
    return p

def slide_title(slide, title, subtitle=None):
    add_rect(slide, Inches(0), Inches(0), prs.slide_width, Inches(1.3), DARK2)
    add_rect(slide, Inches(0), Inches(1.3), prs.slide_width, Inches(0.06), GOLD)
    add_textbox(slide, Inches(0.8), Inches(0.2), Inches(11), Inches(0.7), title, font_size=32, color=WHITE, bold=True)
    if subtitle:
        add_textbox(slide, Inches(0.8), Inches(0.75), Inches(11), Inches(0.5), subtitle, font_size=16, color=LIGHT_GRAY)

def card(slide, left, top, width, height, title, body_lines, icon=""):
    add_rect(slide, left, top, width, height, CARD_BG)
    # subtle gold top border
    add_rect(slide, left, top, width, Inches(0.04), GOLD)
    y = top + Inches(0.25)
    if icon:
        add_textbox(slide, left + Inches(0.25), y, width - Inches(0.5), Inches(0.4), icon, font_size=22, color=GOLD, bold=True)
        y += Inches(0.35)
    add_textbox(slide, left + Inches(0.25), y, width - Inches(0.5), Inches(0.4), title, font_size=18, color=WHITE, bold=True)
    y += Inches(0.4)
    tb = add_textbox(slide, left + Inches(0.25), y, width - Inches(0.5), height - (y - top) - Inches(0.2), "", font_size=14, color=LIGHT_GRAY)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(body_lines):
        if i == 0:
            tf.paragraphs[0].text = line
            tf.paragraphs[0].font.size = Pt(14)
            tf.paragraphs[0].font.color.rgb = LIGHT_GRAY
            tf.paragraphs[0].font.name = 'Calibri'
            tf.paragraphs[0].space_after = Pt(4)
        else:
            add_para(tf, line, font_size=14, color=LIGHT_GRAY)

# ─── SLIDE 1: Portada ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, Inches(0), Inches(0), prs.slide_width, Inches(7.5), RGBColor(0x0D, 0x0D, 0x0D))
# Gold bottom line
add_rect(slide, Inches(0), Inches(6.8), prs.slide_width, Inches(0.08), GOLD)
# Decorative top line
add_rect(slide, Inches(0), Inches(0), prs.slide_width, Inches(0.05), GOLD)
# Central content
add_textbox(slide, Inches(1.5), Inches(1.5), Inches(10), Inches(1.2), "PREDICTOR MUNDIAL FIFA 2026", font_size=44, color=GOLD, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(2), Inches(2.8), Inches(9), Inches(0.6), "Sistema de Predicción Deportiva basado en Machine Learning", font_size=20, color=SOFT_WHITE, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(2), Inches(3.6), Inches(9), Inches(0.6), "Pipeline progresivo · Modelos de clasificación y regresión · Dashboard interactivo", font_size=16, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Simulated trophy silhouette line
add_textbox(slide, Inches(5.5), Inches(5.2), Inches(2.3), Inches(0.5), "🏆", font_size=60, color=GOLD, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(3.5), Inches(6.0), Inches(6.3), Inches(0.4), "Ciencia de Datos · Inteligencia Artificial · Deportes", font_size=14, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# ─── SLIDE 2: Agenda ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "📋 Agenda")
items = [
    ("1. Introducción", "Motivación y objetivos del proyecto"),
    ("2. Datos", "Fuentes, recolección y procesamiento"),
    ("3. Ingeniería de Features", "De los datos crudos a variables predictivas"),
    ("4. Modelos", "Clasificación, regresión y ensemble ponderado"),
    ("5. Pipeline Progresivo", "Fases eliminatorias y validación paso a paso"),
    ("6. Resultados", "Predicciones, precisión y ranking de modelos"),
    ("7. Dashboard", "Visualización interactiva con Streamlit"),
    ("8. Conclusiones", "Hallazgos y trabajo futuro"),
]
y = Inches(1.7)
for title, desc in items:
    add_textbox(slide, Inches(1.5), y, Inches(0.4), Inches(0.35), "▶", font_size=14, color=GOLD)
    add_textbox(slide, Inches(2.0), y, Inches(4), Inches(0.35), title, font_size=18, color=WHITE, bold=True)
    add_textbox(slide, Inches(6.5), y, Inches(5), Inches(0.35), desc, font_size=15, color=LIGHT_GRAY)
    y += Inches(0.55)

# ─── SLIDE 3: Introducción ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "1. Introducción", "Motivación, Objetivo y Alcance")
card(slide, Inches(0.5), Inches(1.7), Inches(6), Inches(2.5), "🎯 Objetivo", [
    "Desarrollar un sistema reproducible de predicción deportiva",
    "basado en Machine Learning para las fases eliminatorias",
    "de la Copa Mundial FIFA 2026.",
    "",
    "El pipeline avanza fase por fase usando únicamente",
    "resultados oficiales ya disputados."
])
card(slide, Inches(7), Inches(1.7), Inches(6), Inches(2.5), "⚽ Motivación", [
    "Demostrar aplicación de ML en análisis deportivo real.",
    "Pipeline progresivo y validado contra resultados oficiales.",
    "Combinación de clasificación (ganador), regresión (marcador)",
    "y modelo de penales.",
    "",
    "No es un simulador tradicional: predice con info real."
])
card(slide, Inches(0.5), Inches(4.5), Inches(6), Inches(2.5), "🏗️ Arquitectura General", [
    "Datos históricos (2014, 2018, 2022) → Feature Engineering",
    "→ Entrenamiento de modelos → predicción progresiva",
    "por fase (R32 → R16 → QF → SF → FINAL).",
    "",
    "Cada fase congela los enfrentamientos oficiales"
])
card(slide, Inches(7), Inches(4.5), Inches(6), Inches(2.5), "📐 Alcance", [
    "6 fases eliminatorias del Mundial 2026",
    "3 modelos de clasificación + 2 regresores + penal",
    "Dashboard interactivo en Streamlit",
    "Reportes automáticos y métricas por fase",
    "Validación contra resultados reales",
])

# ─── SLIDE 4: Tecnologías ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "🛠️ Stack Tecnológico")
techs = [
    ("🐍 Python", "Lenguaje principal del proyecto", "Pandas, NumPy, Scikit-learn"),
    ("🤖 XGBoost", "Gradient Boosting de alto rendimiento", "clasificación y regresión"),
    ("📊 Streamlit", "Dashboard interactivo", "visualización de predicciones y métricas"),
    ("📈 Plotly", "Gráficos interactivos", "curvas de aprendizaje, feature importance"),
    ("💾 Joblib", "Persistencia de modelos", "carga/guardado de pipelines entrenados"),
    ("🧪 Pytest", "Testing automatizado", "validación del pipeline completo"),
]
x_start = 0.5
y_start = 1.7
for i, (name, desc, detail) in enumerate(techs):
    col = i % 3
    row = i // 3
    left = Inches(x_start + col * 4.2)
    top = Inches(y_start + row * 2.8)
    add_rect(slide, left, top, Inches(3.8), Inches(2.4), CARD_BG)
    add_rect(slide, left, top, Inches(3.8), Inches(0.04), GOLD)
    add_textbox(slide, left + Inches(0.2), top + Inches(0.2), Inches(3.4), Inches(0.5), name, font_size=20, color=GOLD, bold=True)
    add_textbox(slide, left + Inches(0.2), top + Inches(0.7), Inches(3.4), Inches(0.4), desc, font_size=15, color=WHITE, bold=False)
    add_textbox(slide, left + Inches(0.2), top + Inches(1.2), Inches(3.4), Inches(0.8), detail, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 5: Datos ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "2. Datos", "Fuentes de información y estructura")
add_textbox(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(0.4), "📂 data/", font_size=18, color=GOLD, bold=True)
add_textbox(slide, Inches(1.5), Inches(2.1), Inches(11), Inches(0.3), "├── raw/    → Datos originales sin procesar", font_size=15, color=WHITE)
add_textbox(slide, Inches(1.5), Inches(2.5), Inches(11), Inches(0.3), "└── processed/ → Datos transformados y predicciones por fase", font_size=15, color=WHITE)
tables = [
    ("historical_matches.csv", "Partidos eliminatorios (2014, 2018, 2022)", "36 registros con marcador, ganador, fase y penales"),
    ("teams_static.csv", "Estadísticas estáticas de selecciones", "Ranking FIFA, historial mundialista, fase de grupos"),
    ("players.csv", "Jugadores clave por selección", "Edad, goles, rating, lesiones, suspensión"),
    ("historical_h2h.csv", "Head-to-Head histórico entre selecciones", "Enfrentamientos directos y resultados"),
    ("bracket_map.json", "Estructura del cuadro eliminatorio", "Mapeo de fases y enfrentamientos"),
    ("official_results.csv", "Resultados oficiales ya disputados", "Actualización conforme avanza el torneo"),
]
y = Inches(3.1)
for name, desc, detail in tables:
    add_rect(slide, Inches(1), y, Inches(11.3), Inches(0.55), CARD_BG)
    add_textbox(slide, Inches(1.2), y + Inches(0.08), Inches(2.8), Inches(0.4), name, font_size=13, color=GOLD, bold=True)
    add_textbox(slide, Inches(4.0), y + Inches(0.08), Inches(4.5), Inches(0.4), desc, font_size=13, color=WHITE)
    add_textbox(slide, Inches(8.5), y + Inches(0.08), Inches(3.8), Inches(0.4), detail, font_size=12, color=LIGHT_GRAY)
    y += Inches(0.6)

# ─── SLIDE 6: Feature Engineering ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "3. Ingeniería de Features", "De los datos crudos a variables predictivas (31 features)")
feat_cats = [
    ("🌍 Ranking y Mundial", "fifa_ranking_pts_diff, fifa_ranking_pos_diff,\nwc_appearances_diff, wc_best_stage_diff, wc_titles_diff"),
    ("⚽ Rendimiento Grupos", "goals_for_group_diff, goals_against_group_diff,\ngroup_strength_score_diff, group_position_a/b"),
    ("🎯 Jugadores Clave", "key_player_availability_diff, top_scorer_goals_diff,\nkey_players_avg_age_diff, prev_wc_goals_diff"),
    ("📊 Estadísticas Técnicas", "possession_avg_diff, shots_on_target_diff,\ndefensive_efficiency_diff, clean_sheets_ko_diff"),
    ("🤝 Head-to-Head", "h2h_wins_a, h2h_wins_b, h2h_draws,\nh2h_goal_diff_avg, h2h_penalties_a_win_rate"),
    ("🏆 Historial Eliminatorio", "ko_stage_historical_win_rate_a/b,\nstage_ordinal, same_confederation, host_advantage"),
]
for i, (cat, feats) in enumerate(feat_cats):
    col = i % 3
    row = i // 3
    left = Inches(0.5 + col * 4.2)
    top = Inches(1.6 + row * 2.9)
    add_rect(slide, left, top, Inches(3.9), Inches(2.6), CARD_BG)
    add_rect(slide, left, top, Inches(3.9), Inches(0.04), GOLD)
    add_textbox(slide, left + Inches(0.2), top + Inches(0.15), Inches(3.5), Inches(0.4), cat, font_size=17, color=GOLD, bold=True)
    add_textbox(slide, left + Inches(0.2), top + Inches(0.6), Inches(3.5), Inches(1.8), feats, font_size=12, color=LIGHT_GRAY)

# ─── SLIDE 7: Modelos ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "4. Modelos de Machine Learning", "Arquitectura de clasificación, regresión y ensemble")

# Classification box
add_rect(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(2.6), CARD_BG)
add_rect(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(5), Inches(0.4), "🤖 Clasificadores (¿Quién avanza?)", font_size=18, color=GOLD, bold=True)
clf_text = (
    "🔹 Logistic Regression — max_iter=2000, balanced\n"
    "🔹 Random Forest — 500 árboles, max_depth=5\n"
    "🔹 XGBoost — 400 árboles, learning_rate=0.03\n\n"
    "Cada modelo genera P(gana Team_A) para cada partido."
)
add_textbox(slide, Inches(0.8), Inches(2.3), Inches(5.4), Inches(1.8), clf_text, font_size=13, color=LIGHT_GRAY)

# Regression box
add_rect(slide, Inches(7), Inches(1.6), Inches(6), Inches(2.6), CARD_BG)
add_rect(slide, Inches(7), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(7.3), Inches(1.8), Inches(5), Inches(0.4), "📈 Regresores (¿Qué marcador?)", font_size=18, color=GOLD, bold=True)
reg_text = (
    "🔹 XGBRegressor (score_a) — count:poisson\n"
    "🔹 XGBRegressor (score_b) — count:poisson\n\n"
    "Predicen goles en tiempo regular (90 min)\n"
    "para cada equipo por separado."
)
add_textbox(slide, Inches(7.3), Inches(2.3), Inches(5.4), Inches(1.8), reg_text, font_size=13, color=LIGHT_GRAY)

# Penalty & Ensemble box
add_rect(slide, Inches(0.5), Inches(4.5), Inches(6), Inches(2.5), CARD_BG)
add_rect(slide, Inches(0.5), Inches(4.5), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(0.8), Inches(4.7), Inches(5), Inches(0.4), "⚖️ Ensemble Ponderado", font_size=18, color=GOLD, bold=True)
ens_text = (
    "Cada clasificador recibe un peso dinámico basado\n"
    "en su accuracy histórica en fases anteriores.\n\n"
    "Pesos iniciales: 1/3 cada uno.\n"
    "Se recalculan tras cada validación (update_stage)."
)
add_textbox(slide, Inches(0.8), Inches(5.2), Inches(5.4), Inches(1.6), ens_text, font_size=13, color=LIGHT_GRAY)

# Penalty box
add_rect(slide, Inches(7), Inches(4.5), Inches(6), Inches(2.5), CARD_BG)
add_rect(slide, Inches(7), Inches(4.5), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(7.3), Inches(4.7), Inches(5), Inches(0.4), "⚠️ Modelo de Penales", font_size=18, color=GOLD, bold=True)
pen_text = (
    "Si el marcador en 90' es empate:\n"
    "  → LogisticRegression sobre features del partido.\n\n"
    "Solo se entrena si hay ≥ 6 partidos con penales\n"
    "en el set de entrenamiento histórico."
)
add_textbox(slide, Inches(7.3), Inches(5.2), Inches(5.4), Inches(1.6), pen_text, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 8: Pipeline ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "5. Pipeline Progresivo", "Flujo de ejecución fase por fase")
stages_data = [
    ("R32", "Dieciseisavos", "Predicción inicial del torneo"),
    ("R16", "Octavos", "Usa resultados oficiales de R32"),
    ("QF", "Cuartos", "Usa resultados oficiales de R16"),
    ("SF", "Semifinales", "Usa resultados oficiales de QF"),
    ("F", "Final", "Usa resultados oficiales de SF"),
]
x = 0.5
for stage, name, desc in stages_data:
    add_rect(slide, Inches(x), Inches(1.6), Inches(2.3), Inches(1.8), CARD_BG)
    add_rect(slide, Inches(x), Inches(1.6), Inches(2.3), Inches(0.04), GOLD)
    add_textbox(slide, Inches(x + 0.1), Inches(1.7), Inches(2.1), Inches(0.4), stage, font_size=22, color=GOLD, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(x + 0.1), Inches(2.15), Inches(2.1), Inches(0.3), name, font_size=14, color=WHITE, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(x + 0.1), Inches(2.5), Inches(2.1), Inches(0.7), desc, font_size=11, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    if stage != "F":
        add_textbox(slide, Inches(x + 2.3), Inches(2.1), Inches(0.3), Inches(0.3), "→", font_size=20, color=GOLD, alignment=PP_ALIGN.CENTER)
    x += 2.6

# Flow description
add_rect(slide, Inches(0.5), Inches(3.7), Inches(12.3), Inches(3.3), CARD_BG)
add_textbox(slide, Inches(0.8), Inches(3.9), Inches(11.5), Inches(0.4), "🔁 Flujo de ejecución", font_size=18, color=GOLD, bold=True)
flow_text = (
    "1. run_stage.py <FASE>   → Predice los partidos de la fase actual usando modelos entrenados con datos históricos\n"
    "2. update_stage.py <FASE> → Valida las predicciones contra resultados oficiales y recalcula pesos del ensemble\n"
    "3. Repite para la siguiente fase hasta llegar a la Final\n\n"
    "🛡️ Mecanismo de guardia: No se puede avanzar a una fase si la anterior no ha sido validada.\n"
    "📊 Por cada fase se genera: reporte JSON, historial de predicciones, comparación vs real, y métricas de accuracy."
)
add_textbox(slide, Inches(0.8), Inches(4.35), Inches(11.5), Inches(2.5), flow_text, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 9: Reporte SF (Semifinales) ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "6. Resultados — Semifinales (SF)", "Predicciones vs resultados oficiales")

# Load data if exists, else show sample
sf_path = "outputs/reports/reporte_SF.json"
try:
    with open(sf_path, encoding="utf-8") as f:
        sf_data = json.load(f)
    matches = sf_data.get("matches", [])
except:
    matches = []

if matches:
    y = Inches(1.6)
    for m in matches:
        add_rect(slide, Inches(0.8), y, Inches(11.5), Inches(0.9), CARD_BG)
        add_rect(slide, Inches(0.8), y, Inches(0.04), Inches(0.9), GOLD)
        add_textbox(slide, Inches(1.1), y + Inches(0.05), Inches(5), Inches(0.4), f"⚔️ {m['team_a']} vs {m['team_b']}", font_size=18, color=WHITE, bold=True)
        winner = m.get("predicted_winner", "")
        prob = m.get("advance_probability_avg_a", 0)
        score = m.get("predicted_score_90", {})
        add_textbox(slide, Inches(1.1), y + Inches(0.45), Inches(5), Inches(0.4), f"Ganador: {winner} · Prob: {prob:.1%} · Score: {score.get('a',0)}-{score.get('b',0)}", font_size=13, color=LIGHT_GRAY)

        # Model probs
        ap = m.get("advance_probability", {})
        add_textbox(slide, Inches(6.5), y + Inches(0.1), Inches(2), Inches(0.3), f"LR: {ap.get('logreg',0):.0%}", font_size=12, color=GREEN_ACCENT)
        add_textbox(slide, Inches(6.5), y + Inches(0.4), Inches(2), Inches(0.3), f"RF: {ap.get('random_forest',0):.0%}", font_size=12, color=BLUE_ACCENT)
        add_textbox(slide, Inches(6.5), y + Inches(0.7), Inches(2), Inches(0.3), f"XGB: {ap.get('xgboost',0):.0%}", font_size=12, color=RED_ACCENT)

        actual = m.get("actual_result")
        if actual:
            add_textbox(slide, Inches(9.5), y + Inches(0.2), Inches(3), Inches(0.3), f"✓ Real: {actual.get('winner','')} ({actual.get('score_90',{}).get('a',0)}-{actual.get('score_90',{}).get('b',0)})", font_size=13, color=GREEN_ACCENT)
            hit = m.get("hit", False)
            if hit:
                add_textbox(slide, Inches(9.5), y + Inches(0.5), Inches(2), Inches(0.3), "✅ ACERTADO", font_size=14, color=GREEN_ACCENT, bold=True)
            else:
                add_textbox(slide, Inches(9.5), y + Inches(0.5), Inches(2), Inches(0.3), "❌ FALLADO", font_size=14, color=RED_ACCENT, bold=True)
        else:
            add_textbox(slide, Inches(9.5), y + Inches(0.4), Inches(2.5), Inches(0.3), "⏳ Pendiente", font_size=13, color=LIGHT_GRAY)
        y += Inches(1.0)

    # Summary
    acc = sf_data.get("prediction_accuracy", 0)
    hits = sf_data.get("prediction_hits", 0)
    total = sf_data.get("prediction_matches", 0)
    add_rect(slide, Inches(0.8), y + Inches(0.1), Inches(11.5), Inches(0.6), CARD_BG)
    add_textbox(slide, Inches(1.1), y + Inches(0.2), Inches(11), Inches(0.4), f"📊 Accuracy: {acc:.2%} · Aciertos: {hits}/{total} · Training set: {sf_data.get('train_set_size',0)} partidos históricos", font_size=15, color=GOLD, bold=True)
else:
    add_textbox(slide, Inches(1), Inches(2), Inches(10), Inches(0.5), "Datos de Semifinales disponibles para visualización.", font_size=18, color=WHITE)
    add_textbox(slide, Inches(1), Inches(2.8), Inches(10), Inches(3), 
        "Ejemplo de predicción:\n\n"
        "  FRA vs ESP → Ganador: FRA (87.6%) · Score: 1-1 · Penal: 99.4%\n"
        "  ENG vs ARG → Ganador: ARG (80.5%) · Score: 1-1 · Penal: 31.9%\n\n"
        "📊 Los pesos del ensemble se recalculan según accuracy histórica de cada modelo.\n"
        "📈 Los reportes incluyen feature importance y comparación con resultados reales.",
        font_size=14, color=LIGHT_GRAY)

# ─── SLIDE 10: Feature Importance ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "7. Importancia de Features", "¿Qué variables influyen más en las predicciones?")
try:
    top_feats = sf_data.get("top_features", {})
except:
    top_feats = {}
if top_feats:
    models_display = {"logreg": "Logistic Regression", "random_forest": "Random Forest", "xgboost": "XGBoost"}
    cols = [0.5, 4.8, 9.1]
    for idx, (mkey, mlabel) in enumerate(models_display.items()):
        left = Inches(cols[idx])
        add_textbox(slide, left, Inches(1.6), Inches(4), Inches(0.4), mlabel, font_size=16, color=GOLD, bold=True)
        feats = top_feats.get(mkey, [])
        y = Inches(2.1)
        for feat_name, imp_val in feats:
            add_rect(slide, left, y, Inches(3.8), Inches(0.35), CARD_BG)
            add_textbox(slide, left + Inches(0.1), y + Inches(0.02), Inches(2.5), Inches(0.3), feat_name, font_size=11, color=WHITE)
            # bar
            bar_max = max(abs(v) for _, v in feats) if feats else 1
            bar_w = Inches(1.0 * abs(imp_val) / bar_max)
            bar_color = GREEN_ACCENT if imp_val > 0 else RED_ACCENT
            if bar_w > Inches(0):
                add_rect(slide, left + Inches(2.6), y + Inches(0.07), bar_w, Inches(0.2), bar_color)
            add_textbox(slide, left + Inches(2.6) + bar_w + Inches(0.05), y + Inches(0.02), Inches(0.8), Inches(0.3), f"{imp_val:.3f}", font_size=10, color=LIGHT_GRAY)
            y += Inches(0.4)
else:
    add_textbox(slide, Inches(1), Inches(2), Inches(11), Inches(3),
        "Feature Importance mide cuánto contribuye cada variable a la decisión del modelo.\n\n"
        "🔹 Logistic Regression: Coeficientes de la regresión (positivo → favorece a equipo A)\n"
        "🔹 Random Forest / XGBoost: Importancia por ganancia de información\n\n"
        "Features más relevantes:\n"
        "  • ko_stage_historical_win_rate_a/b — Tasa de victorias en KO histórica\n"
        "  • key_players_prev_wc_goals_diff — Goles previos de jugadores clave\n"
        "  • fifa_ranking_pos_diff — Diferencia en ranking FIFA\n"
        "  • wc_best_stage_diff — Mejor fase histórica alcanzada",
        font_size=14, color=LIGHT_GRAY)

# ─── SLIDE 11: Dashboard ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "8. Dashboard Interactivo", "Visualización con Streamlit + Plotly")

sections = [
    ("📊 Resumen", "Vista general del torneo, predicciones y accuracy por fase"),
    ("⚽ Predicciones", "Listado de partidos con marcador, probabilidad y ganador"),
    ("🤖 Modelos", "Comparación entre Logistic Regression, RF y XGBoost"),
    ("🔍 Explicabilidad", "Feature importance y SHAP values por fase"),
    ("📈 Métricas", "Evolución de accuracy, F1-score y error a lo largo del torneo"),
    ("📜 Historial", "Histórico completo de predicciones vs resultados oficiales"),
    ("🌳 Árbol del Mundial", "Cuadro eliminatorio interactivo con predicciones"),
    ("⚙️ Configuración", "Parámetros del pipeline y control de ejecución"),
]
for i, (icon_title, desc) in enumerate(sections):
    col = i % 4
    row = i // 4
    left = Inches(0.5 + col * 3.2)
    top = Inches(1.6 + row * 2.9)
    add_rect(slide, left, top, Inches(2.9), Inches(2.5), CARD_BG)
    add_rect(slide, left, top, Inches(2.9), Inches(0.04), GOLD)
    add_textbox(slide, left + Inches(0.15), top + Inches(0.15), Inches(2.6), Inches(0.4), icon_title, font_size=16, color=GOLD, bold=True)
    add_textbox(slide, left + Inches(0.15), top + Inches(0.65), Inches(2.6), Inches(1.5), desc, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 12: Métricas ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "9. Evaluación y Métricas", "Accuracy, Precision, Recall, F1-Score por modelo")
add_textbox(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(0.4), "📋 Cada fase genera automáticamente:", font_size=18, color=GOLD, bold=True)
metrics_list = [
    "Reporte JSON con predicciones detalladas de cada partido",
    "Matriz de validación: accuracy, precision, recall y F1 por cada clasificador",
    "Ranking de modelos ordenados por rendimiento",
    "Selección automática del mejor clasificador para la fase",
    "Comparación predicción vs resultado real (hit/miss)",
    "Historial de métricas acumulado (metrics_history.csv)",
    "Predicción histórica completa (prediction_history.csv)",
]
y = Inches(2.2)
for m in metrics_list:
    add_textbox(slide, Inches(1.2), y, Inches(11), Inches(0.3), f"▸ {m}", font_size=14, color=LIGHT_GRAY)
    y += Inches(0.4)

add_rect(slide, Inches(0.5), y + Inches(0.2), Inches(12.3), Inches(2.0), CARD_BG)
add_textbox(slide, Inches(0.8), y + Inches(0.35), Inches(11.5), Inches(0.4), "🎯 Métricas Clave", font_size=18, color=GOLD, bold=True)
metric_boxes = [
    ("Accuracy", "% de aciertos en predicción del ganador"),
    ("Precision", "De los que predijo como ganador, cuántos acertó"),
    ("Recall", "De los ganadores reales, cuántos predijo"),
    ("F1-Score", "Media armónica de precision y recall"),
    ("MAE / RMSE", "Error absoluto/raíz en predicción de marcadores"),
]
x = 0.8
for met, desc in metric_boxes:
    add_textbox(slide, Inches(x), y + Inches(0.8), Inches(2.2), Inches(0.3), met, font_size=14, color=WHITE, bold=True)
    add_textbox(slide, Inches(x), y + Inches(1.15), Inches(2.2), Inches(0.5), desc, font_size=11, color=LIGHT_GRAY)
    x += 2.4

# ─── SLIDE 13: Validación ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "10. Validación Automática", "Mecanismo de integridad del pipeline")
add_rect(slide, Inches(0.5), Inches(1.6), Inches(5.8), Inches(5.3), CARD_BG)
add_rect(slide, Inches(0.5), Inches(1.6), Inches(5.8), Inches(0.04), GOLD)
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(5.2), Inches(0.4), "🛡️ advance_to_next_stage_guard()", font_size=18, color=GOLD, bold=True)
guard_text = (
    "Impide avanzar a la siguiente fase si:\n\n"
    "1. No existen todos los resultados oficiales\n"
    "   necesarios para armar los enfrentamientos.\n\n"
    "2. La fase anterior aún no ha sido evaluada\n"
    "   con update_stage.py.\n\n"
    "Mensaje típico:\n"
    "  [DETENIDO] La fase R16 aún no ha sido evaluada.\n"
    "  Ejecute primero:\n"
    "  python scripts/update_stage.py R16"
)
add_textbox(slide, Inches(0.8), Inches(2.3), Inches(5.2), Inches(4.2), guard_text, font_size=13, color=LIGHT_GRAY)

add_rect(slide, Inches(6.8), Inches(1.6), Inches(6), Inches(5.3), CARD_BG)
add_rect(slide, Inches(6.8), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(7.1), Inches(1.8), Inches(5.4), Inches(0.4), "⚖️ Pesos Dinámicos del Ensemble", font_size=18, color=GOLD, bold=True)
weight_text = (
    "Los clasificadores se ponderan según su\n"
    "accuracy demostrada en fases previas:\n\n"
    "  Peso_m = accuracy_m / Σ accuracy_total\n\n"
    "Ejemplo tras validación de R32:\n"
    "  LR:  0.500 → Peso: 0.27\n"
    "  RF:  0.500 → Peso: 0.27\n"
    "  XGB: 0.833 → Peso: 0.46\n\n"
    "Esto permite que el modelo más fiable tenga\n"
    "mayor influencia en la predicción final."
)
add_textbox(slide, Inches(7.1), Inches(2.3), Inches(5.4), Inches(4.2), weight_text, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 14: Estructura del Proyecto ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "11. Estructura del Proyecto", "Organización del código y los datos")
tree_text = (
    "mundial2026_predictor/\n"
    "├── dashboard/          → Aplicación Streamlit (8 páginas)\n"
    "│   ├── app.py          → Página principal\n"
    "│   ├── styles.py       → Estilos CSS personalizados\n"
    "│   ├── flags.py        → Banderas de selecciones\n"
    "│   └── pages/          → Módulos del dashboard\n"
    "├── data/               → Datos del torneo\n"
    "│   ├── raw/            → Datos originales (CSV, JSON)\n"
    "│   └── processed/      → Predicciones y comparaciones\n"
    "├── outputs/            → Reportes, logs e históricos\n"
    "├── saved_models/       → Modelos entrenados (.joblib)\n"
    "├── scripts/            → Scripts de ejecución\n"
    "│   ├── run_stage.py    → Ejecutar predicción de fase\n"
    "│   ├── update_stage.py → Validar fase con resultados\n"
    "│   └── train_models.py → Entrenar modelos\n"
    "├── src/                → Código fuente del pipeline\n"
    "│   ├── pipeline.py     → Orquestador principal\n"
    "│   ├── models.py       → Definición de modelos\n"
    "│   ├── feature_engineering.py → Construcción de features\n"
    "│   └── ...\n"
    "└── tests/              → Pruebas unitarias"
)
add_rect(slide, Inches(0.5), Inches(1.6), Inches(12.3), Inches(5.3), CARD_BG)
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0), tree_text, font_size=12, color=LIGHT_GRAY)

# ─── SLIDE 15: Cómo ejecutar ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "12. ¿Cómo Ejecutar?", "Comandos para correr el pipeline")
add_rect(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(2.5), CARD_BG)
add_rect(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(5.4), Inches(0.4), "▶️ Predecir una fase", font_size=18, color=GOLD, bold=True)
cmd_run = (
    "# Entrenar modelos\n"
    "python scripts/train_models.py\n\n"
    "# Predecir una fase\n"
    "python scripts/run_stage.py R32\n"
    "python scripts/run_stage.py R16\n"
    "python scripts/run_stage.py QF\n"
    "python scripts/run_stage.py SF\n"
    "python scripts/run_stage.py FINAL"
)
add_textbox(slide, Inches(0.8), Inches(2.3), Inches(5.4), Inches(1.6), cmd_run, font_size=13, color=GREEN_ACCENT)

add_rect(slide, Inches(7), Inches(1.6), Inches(6), Inches(2.5), CARD_BG)
add_rect(slide, Inches(7), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(7.3), Inches(1.8), Inches(5.4), Inches(0.4), "✅ Validar una fase", font_size=18, color=GOLD, bold=True)
cmd_update = (
    "# Validar predicciones contra resultados\n"
    "python scripts/update_stage.py R32\n"
    "python scripts/update_stage.py R16\n"
    "python scripts/update_stage.py QF\n"
    "python scripts/update_stage.py SF\n"
    "python scripts/update_stage.py FINAL\n\n"
    "# Dashboard interactivo\n"
    "streamlit run dashboard/app.py"
)
add_textbox(slide, Inches(7.3), Inches(2.3), Inches(5.4), Inches(1.6), cmd_update, font_size=13, color=GREEN_ACCENT)

add_rect(slide, Inches(0.5), Inches(4.4), Inches(12.3), Inches(2.6), CARD_BG)
add_textbox(slide, Inches(0.8), Inches(4.6), Inches(11.5), Inches(0.4), "🧪 Tests", font_size=18, color=GOLD, bold=True)
add_textbox(slide, Inches(0.8), Inches(5.1), Inches(11.5), Inches(0.3), "pytest -q    # Ejecuta todas las pruebas unitarias", font_size=14, color=GREEN_ACCENT)
add_textbox(slide, Inches(0.8), Inches(5.6), Inches(11.5), Inches(0.8),
    "Los modelos se guardan en saved_models/ y se reutilizan entre ejecuciones.\n"
    "Si se agregan nuevos datos históricos, se pueden reentrenar con train_models.py",
    font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 16: Conclusiones ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
slide_title(slide, "13. Conclusiones y Trabajo Futuro")
add_rect(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(5.3), CARD_BG)
add_rect(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(5.4), Inches(0.4), "✅ Logros", font_size=18, color=GOLD, bold=True)
logros = (
    "✔ Pipeline completo y reproducible para las 6 fases\n\n"
    "✔ Ensemble adaptable con pesos dinámicos\n\n"
    "✔ Validación automática contra resultados reales\n\n"
    "✔ Dashboard interactivo con 8 secciones\n\n"
    "✔ Feature engineering con 31 variables\n\n"
    "✔ Cobertura de tests con pytest\n\n"
    "✔ Persistencia de modelos (joblib)"
)
add_textbox(slide, Inches(0.8), Inches(2.3), Inches(5.4), Inches(4.2), logros, font_size=13, color=LIGHT_GRAY)

add_rect(slide, Inches(6.9), Inches(1.6), Inches(6), Inches(5.3), CARD_BG)
add_rect(slide, Inches(6.9), Inches(1.6), Inches(6), Inches(0.04), GOLD)
add_textbox(slide, Inches(7.2), Inches(1.8), Inches(5.4), Inches(0.4), "🔮 Trabajo Futuro", font_size=18, color=GOLD, bold=True)
futuro = (
  "• Incorporar datos de lesiones en tiempo real\n\n"
  "• Modelo de Deep Learning (redes neuronales)\n\n"
  "• Predicción de formación táctica (XI inicial)\n\n"
  "• Análisis de odds de casas de apuestas\n\n"
  "• Simulación Monte Carlo para distribución de\n"
  "  probabilidades del torneo completo\n\n"
  "• Soporte para más torneos (Copa América, Eurocopa)"
)
add_textbox(slide, Inches(7.2), Inches(2.3), Inches(5.4), Inches(4.2), futuro, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 17: Gracias ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, Inches(0), Inches(0), prs.slide_width, Inches(0.05), GOLD)
add_rect(slide, Inches(0), Inches(7.45), prs.slide_width, Inches(0.05), GOLD)
add_textbox(slide, Inches(1), Inches(2.0), Inches(11), Inches(1.0), "GRACIAS", font_size=56, color=GOLD, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(1), Inches(3.2), Inches(11), Inches(0.6), "Predictor Mundial FIFA 2026", font_size=24, color=WHITE, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(2), Inches(4.0), Inches(9), Inches(0.5), "Machine Learning aplicado al análisis deportivo", font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(2), Inches(5.0), Inches(9), Inches(0.5), "📧 Ciencia de Datos · IA · Deportes", font_size=16, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(3), Inches(6.0), Inches(7), Inches(0.4), "⚽🏆⚽", font_size=40, color=GOLD, alignment=PP_ALIGN.CENTER)

# ─── Save ───
output_path = os.path.join(os.path.dirname(__file__), "Presentacion_Predictor_Mundial_2026.pptx")
prs.save(output_path)
print(f"Presentación creada: {output_path}")
