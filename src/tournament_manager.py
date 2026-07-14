from src.stage_generator import generate_next_stage

NEXT_STAGE = {
    "R32": "R16",
    "R16": "QF",
    "QF": "SF",
    "SF": "F",
    "3P": None,
    "F": None,
}


def advance_tournament(stage: str):

    if stage not in NEXT_STAGE:
        return None

    generate_next_stage(stage)

    return NEXT_STAGE[stage]