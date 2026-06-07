import pandas as pd
import random


def generate_family_sizes(num_families: int):

    rows = []

    family_sizes = [1, 2, 3, 4, 5, 6, 7]

    weights = [
        0.02,  # 1
        0.05,  # 2
        0.10,  # 3
        0.20,  # 4
        0.30,  # 5
        0.20,  # 6
        0.13   # 7
    ]

    for family_id in range(1, num_families + 1):

        size = random.choices(
            family_sizes,
            weights=weights
        )[0]

        rows.append({
            "family_id": family_id,
            "family_size": size
        })

    return pd.DataFrame(rows)