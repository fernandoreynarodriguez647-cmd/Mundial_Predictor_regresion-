# ⚽ Predictor Mundial FIFA 2026

> Pipeline de Machine Learning para predecir las fases eliminatorias de la Copa Mundial FIFA 2026 mediante un flujo progresivo basado en resultados oficiales.

---

# 📖 Descripción

**Predictor Mundial FIFA 2026** es un proyecto de Ciencia de Datos que automatiza la predicción de las fases eliminatorias del Mundial utilizando modelos de Machine Learning entrenados con información histórica de las ediciones **2014, 2018 y 2022**.

A diferencia de un simulador tradicional, este proyecto **no predice todo el torneo desde el inicio**. El pipeline avanza conforme se disputan los partidos oficiales, garantizando que cada nueva predicción utilice únicamente información real del torneo.

---

# ✨ Características

* ⚽ Predicción progresiva de todas las fases eliminatorias.
* 🤖 Modelos de clasificación para estimar el ganador.
* 📈 Modelos de regresión para estimar el marcador.
* 🔄 Actualización automática conforme se publican los resultados oficiales.
* 📊 Evaluación automática del rendimiento de los modelos.
* 📑 Generación de reportes y métricas.
* 🖥 Dashboard interactivo desarrollado con Streamlit.
* ✅ Pipeline completamente reproducible.

---

# 📊 Resultados Oficiales del Mundial 2026

## 🥇 Dieciseisavos de Final (R32)

| Partido | Equipo A | Marcador | Equipo B | ¿Penales? | Ganador |
|:-------:|:--------:|:--------:|:--------:|:---------:|:-------:|
| M73 | RSA | 0 – 1 | **CAN** | No | 🇨🇦 CAN |
| M74 | GER | 1 – 1 | **PAR** | Sí (4-3) | 🇵🇾 PAR |
| M75 | NED | 1 – 1 | **MAR** | Sí (3-5) | 🇲🇦 MAR |
| M76 | BRA | 2 – 1 | JPN | No | 🇧🇷 BRA |
| M77 | FRA | 3 – 0 | SWE | No | 🇫🇷 FRA |
| M78 | CIV | 1 – 2 | **NOR** | No | 🇳🇴 NOR |
| M79 | MEX | 2 – 0 | ECU | No | 🇲🇽 MEX |
| M80 | ENG | 2 – 1 | COD | No | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG |
| M81 | USA | 2 – 0 | BIH | No | 🇺🇸 USA |
| M82 | BEL | 2 – 2 | SEN | No | 🇧🇪 BEL |
| M83 | POR | 2 – 1 | CRO | No | 🇵🇹 POR |
| M84 | ESP | 3 – 0 | AUT | No | 🇪🇸 ESP |
| M85 | SUI | 2 – 0 | ALG | No | 🇨🇭 SUI |
| M86 | ARG | 1 – 1 | CPV | No | 🇦🇷 ARG |
| M87 | COL | 1 – 0 | GHA | No | 🇨🇴 COL |
| M88 | AUS | 1 – 1 | **EGY** | Sí (3-5) | 🇪🇬 EGY |

**Clasificados a Octavos:** 🇨🇦 CAN · 🇵🇾 PAR · 🇲🇦 MAR · 🇧🇷 BRA · 🇫🇷 FRA · 🇳🇴 NOR · 🇲🇽 MEX · 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG · 🇺🇸 USA · 🇧🇪 BEL · 🇵🇹 POR · 🇪🇸 ESP · 🇨🇭 SUI · 🇦🇷 ARG · 🇨🇴 COL · 🇪🇬 EGY

---

## 🥈 Octavos de Final (R16)

| Partido | Equipo A | Marcador | Equipo B | ¿Penales? | Ganador |
|:-------:|:--------:|:--------:|:--------:|:---------:|:-------:|
| M89 | PAR | 0 – 1 | **FRA** | No | 🇫🇷 FRA |
| M90 | CAN | 0 – 3 | **MAR** | No | 🇲🇦 MAR |
| M91 | BRA | 1 – 2 | **NOR** | No | 🇳🇴 NOR |
| M92 | MEX | 2 – 3 | **ENG** | No | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG |
| M93 | POR | 0 – 1 | **ESP** | No | 🇪🇸 ESP |
| M94 | USA | 1 – 4 | **BEL** | No | 🇧🇪 BEL |
| M95 | ARG | 3 – 2 | EGY | No | 🇦🇷 ARG |
| M96 | SUI | 0 – 0 | COL | Sí | 🇨🇭 SUI |

**Clasificados a Cuartos:** 🇫🇷 FRA · 🇲🇦 MAR · 🇳🇴 NOR · 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG · 🇪🇸 ESP · 🇧🇪 BEL · 🇦🇷 ARG · 🇨🇭 SUI

---

## 🥉 Cuartos de Final (QF)

| Partido | Equipo A | Marcador | Equipo B | ¿Penales? | Ganador |
|:-------:|:--------:|:--------:|:--------:|:---------:|:-------:|
| M97 | FRA | 2 – 0 | MAR | No | 🇫🇷 FRA |
| M98 | ESP | 2 – 1 | BEL | No | 🇪🇸 ESP |
| M99 | NOR | 1 – 1 | **ENG** | No | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG |
| M100 | ARG | 1 – 1 | **SUI** | No | 🇦🇷 ARG |

**Clasificados a Semifinales:** 🇫🇷 FRA · 🇪🇸 ESP · 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG · 🇦🇷 ARG

---

## 🏅 Semifinales (SF) — Predicciones

| Partido | Equipo A | vs | Equipo B | Ganador Predicho |
|:-------:|:--------:|:--:|:--------:|:----------------:|
| M101 | 🇫🇷 FRA | vs | 🇪🇸 ESP | 🇫🇷 FRA |
| M102 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG | vs | 🇦🇷 ARG | 🇦🇷 ARG |

> ⏳ Partidos aún no disputados. Resultados pendientes de confirmación.

---

# 🧠 Modelos utilizados

## Clasificación

* Logistic Regression
* Random Forest
* XGBoost

Estos modelos predicen qué selección tiene mayor probabilidad de avanzar.

## Regresión

Modelos de regresión utilizados para estimar el marcador esperado antes de una posible definición por penales.

---

# 📂 Estructura del proyecto

```text
mundial2026_predictor/
│
├── dashboard/
├── data/
├── outputs/
│   ├── history/
│   ├── reports/
│   └── logs/
├── saved_models/
├── scripts/
├── src/
├── tests/
├── requirements.txt
└── README.md
```

---

# 🚀 Flujo de ejecución

El proyecto sigue un flujo secuencial. **No es posible ejecutar una fase si la anterior aún no ha sido validada con resultados oficiales.**

## 🥇 Fase 1 — Dieciseisavos de Final (R32)

Genera la predicción inicial del torneo.

```bash
python scripts/run_stage.py R32
```

Al finalizar los partidos oficiales:

```bash
python scripts/update_stage.py R32
```

Luego continúa con:

```bash
python scripts/run_stage.py R16
```

---

## 🥈 Fase 2 — Octavos de Final (R16)

Las predicciones utilizan exclusivamente los equipos clasificados oficialmente desde R32.

```bash
python scripts/run_stage.py R16
```

Cuando finalicen los partidos:

```bash
python scripts/update_stage.py R16
```

Continuar:

```bash
python scripts/run_stage.py QF
```

---

## 🥉 Fase 3 — Cuartos de Final (QF)

El pipeline vuelve a reconstruir el cuadro utilizando únicamente los resultados oficiales de Octavos.

```bash
python scripts/run_stage.py QF
```

Después:

```bash
python scripts/update_stage.py QF
```

Continuar:

```bash
python scripts/run_stage.py SF
```

---

## 🏅 Fase 4 — Semifinales (SF)

```bash
python scripts/run_stage.py SF
```

Cuando existan resultados oficiales:

```bash
python scripts/update_stage.py SF
```

Continuar:

```bash
python scripts/run_stage.py FINAL
```

---

## 🏆 Fase 5 — Final

```bash
python scripts/run_stage.py FINAL
```

Después del partido:

```bash
python scripts/update_stage.py FINAL
```

El sistema genera el reporte final del torneo y las métricas globales.

---

# 🔒 Validación automática

El pipeline impide avanzar si una fase anterior no ha sido evaluada.

Por ejemplo:

```text
[DETENIDO] La fase R16 aún no ha sido evaluada.

Ejecute primero:

python scripts/update_stage.py R16
```

Este mecanismo garantiza que las predicciones siempre utilicen resultados oficiales y que el cuadro eliminatorio permanezca consistente durante todo el torneo.

---

# 📊 Archivos generados

Después de cada fase se generan automáticamente:

```text
outputs/

├── reports/
│   ├── reporte_R32.json
│   ├── reporte_R16.json
│   ├── reporte_QF.json
│   ├── reporte_SF.json
│   └── reporte_FINAL.json
│
├── history/
│   ├── metrics_history.csv
│   └── prediction_history.csv
│
└── logs/
```

---

# 🧪 Ejecutar pruebas

```bash
pytest -q
```

---

# 🛠 Tecnologías

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Streamlit
* Plotly
* Joblib
* Pytest

---

# 📈 Flujo del proyecto

```text
Resultados históricos (2014, 2018 y 2022)
                │
                ▼
     Ingeniería de características
                │
                ▼
 Entrenamiento de modelos ML
                │
                ▼
Predicción de Dieciseisavos (R32)
                │
                ▼
Resultados oficiales
                │
                ▼
 Validación (update_stage.py)
                │
                ▼
Predicción de Octavos (R16)
                │
                ▼
Resultados oficiales
                │
                ▼
 Validación (update_stage.py)
                │
                ▼
Predicción de Cuartos (QF)
                │
                ▼
Resultados oficiales
                │
                ▼
Predicción de Semifinales (SF)
                │
                ▼
Resultados oficiales
                │
                ▼
Predicción de la Final
                │
                ▼
Reporte final y métricas
```

---

# 🎯 Objetivo

Desarrollar un sistema reproducible de predicción deportiva basado en Machine Learning que permita simular y evaluar las fases eliminatorias de la Copa Mundial FIFA 2026 utilizando únicamente información oficial disponible en cada etapa del torneo.

---

# 👥 Integrantes del Grupo

| N° | Integrante |
|:--:|:-----------|
| 1 | Puerta Culqui Leydi Marlith |
| 2 | Huaman Huaman Lilian Janet |
| 3 | Perez Silva Jhohan |
| 4 | Vin Zumaeta Willy |
| 5 | Reyna Rodriguez Fernando |

---

# 📄 Licencia

Este proyecto fue desarrollado con fines educativos y de investigación en Ciencia de Datos y Machine Learning aplicado al análisis deportivo.
