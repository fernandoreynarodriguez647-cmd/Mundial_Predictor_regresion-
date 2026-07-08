from src import data_loader as dl


def generate_stage(stage, bracket_map, official_results):
    """
    Genera los enfrentamientos de una fase utilizando
    únicamente los resultados oficiales disponibles.
    """

    return dl.get_stage_fixtures(
        stage,
        bracket_map,
        official_results,
    )