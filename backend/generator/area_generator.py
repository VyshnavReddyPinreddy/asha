from faker import Faker
import pandas as pd
import random

fake = Faker("en_IN")


def generate_health_areas(num_areas: int, num_anms: int):

    area_types = (
        ["VILLAGE"] * 300 +
        ["WARD"] * 100 +
        ["COLONY"] * 70 +
        ["SLUM"] * 30
    )

    random.shuffle(area_types)

    rows = []

    for area_id in range(1, num_areas + 1):

        anm_id = ((area_id - 1) % num_anms) + 1

        rows.append({
            "area_id": area_id,
            "area_name": f"{fake.city()} Area {area_id}",
            "area_type": area_types[area_id - 1],
            "mandal": fake.city(),
            "district": fake.state(),
            "anm_id": anm_id
        })

    return pd.DataFrame(rows)