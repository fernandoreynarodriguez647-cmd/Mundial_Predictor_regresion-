import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import config as cfg


def main():

    if len(sys.argv) != 2:
        print("Uso:")
        print("python scripts/update_stage.py R16")
        return

    stage = cfg.validate_stage(sys.argv[1])

    report_file = cfg.REPORTS / f"reporte_{stage}.json"
    official_file = cfg.DATA_RAW / "official_results.csv"

    if not report_file.exists():
        raise FileNotFoundError(report_file)

    report = json.loads(report_file.read_text(encoding="utf8"))

    official = pd.read_csv(official_file)
    official = official[official.stage == stage]

    hits = 0
    comparison = []

    for match in report["matches"]:

        real = official[official.match_id == match["match_id"]]

        if real.empty:
            continue

        real = real.iloc[0]

        correct = match["predicted_winner"] == real["winner_final"]

        if correct:
            hits += 1

        comparison.append(
            {
                "match_id": match["match_id"],
                "team_a": match["team_a"],
                "team_b": match["team_b"],
                "predicted": match["predicted_winner"],
                "official": real["winner_final"],
                "correct": correct,
            }
        )

    df = pd.DataFrame(comparison)

    comparison_file = cfg.DATA_PROCESSED / f"{stage}_comparison.csv"
    df.to_csv(comparison_file, index=False)

    report["prediction_matches"] = len(df)
    report["prediction_hits"] = hits
    report["prediction_misses"] = len(df) - hits

    if len(df):
        report["prediction_accuracy"] = round(hits / len(df), 4)
    else:
        report["prediction_accuracy"] = 0

    # =====================================================
    # Guardar historial del rendimiento por fase
    # =====================================================

    history_file = cfg.OUTPUTS / "prediction_history.csv"

    new_row = pd.DataFrame(
        [
            {
                "stage": stage,
                "matches": len(df),
                "hits": hits,
                "misses": len(df) - hits,
                "accuracy": report["prediction_accuracy"],
            }
        ]
    )

    if history_file.exists():

        history = pd.read_csv(history_file)

        # Evitar duplicar la misma fase
        history = history[history["stage"] != stage]

        history = pd.concat([history, new_row], ignore_index=True)

    else:

        history = new_row

    history.to_csv(history_file, index=False)

    # =====================================================
    # Actualizar reporte JSON
    # =====================================================

    report_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf8",
    )

    # =====================================================
    # Mostrar comparación
    # =====================================================

    print("\n========== COMPARACIÓN ==========")

    for row in comparison:

        estado = "✔" if row["correct"] else "✘"

        print(
            f"{estado} "
            f"{row['match_id']} | "
            f"{row['team_a']} vs {row['team_b']} | "
            f"Predicción: {row['predicted']} | "
            f"Oficial: {row['official']}"
        )

    # =====================================================
    # Resumen
    # =====================================================

    print("\n=========== RESUMEN ===========")

    print(f"Fase      : {stage}")
    print(f"Partidos  : {len(df)}")
    print(f"Aciertos  : {hits}")
    print(f"Fallos    : {len(df)-hits}")
    print(f"Accuracy  : {report['prediction_accuracy']:.2%}")

    print("\nHistorial actualizado:")
    print(history_file)

    print("===============================")


if __name__ == "__main__":
    main()