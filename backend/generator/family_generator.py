import pandas as pd
import random


def generate_families(num_families: int, num_areas: int):

    house_types = [
        "PUCCA",
        "SEMI_PUCCA",
        "KUTCHA"
    ]

    socio_categories = [
        "LOW",
        "MIDDLE",
        "HIGH"
    ]

    rows = []

    for family_id in range(1, num_families + 1):

        area_id = ((family_id - 1) % num_areas) + 1

        rows.append({
            "family_id": family_id,
            "area_id": area_id,
            "house_number": f"H-{family_id}",
            "house_type": random.choices(
                house_types,
                weights=[60, 25, 15]
            )[0],
            "has_toilet": random.choices(
                [True, False],
                weights=[85, 15]
            )[0],
            "socio_economic_category": random.choices(
                socio_categories,
                weights=[25, 60, 15]
            )[0]
        })

    return pd.DataFrame(rows)