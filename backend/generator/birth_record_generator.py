# birth_record_generator.py

import pandas as pd
import random


def generate_birth_records(
    pregnancy_df,
    newborn_df
):

    completed = pregnancy_df[
        pregnancy_df["pregnancy_status"] == "COMPLETED"
    ]

    births = []

    for birth_id, (
        (_, preg),
        (_, baby)
    ) in enumerate(
        zip(
            completed.iterrows(),
            newborn_df.iterrows()
        ),
        start=1
    ):

        births.append({

            "birth_id":
                birth_id,

            "pregnancy_id":
                preg["pregnancy_id"],

            "child_id":
                baby["person_id"],

            "birth_weight_kg":
                round(
                    random.uniform(
                        2.3,
                        4.2
                    ),
                    2
                ),

            "delivery_type":
                random.choices(
                    [
                        "NORMAL",
                        "C_SECTION"
                    ],
                    weights=[
                        75,
                        25
                    ]
                )[0],

            "remarks":
                "Healthy birth"
        })

    return pd.DataFrame(births)