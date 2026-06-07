import pandas as pd
import random


def generate_person_diseases(
    person_df,
    num_records=75000
):

    diseases = list(range(1, 31))

    records = []

    used = set()

    person_ids = (
        person_df["person_id"]
        .tolist()
    )

    while len(records) < num_records:

        person_id = random.choice(
            person_ids
        )

        disease_id = random.choice(
            diseases
        )

        key = (
            person_id,
            disease_id
        )

        if key in used:
            continue

        used.add(key)

        records.append({

            "person_disease_id":
                len(records) + 1,

            "person_id":
                person_id,

            "disease_id":
                disease_id,

            "diagnosis_date":
                pd.Timestamp.today()
                -
                pd.Timedelta(
                    days=random.randint(
                        0,
                        3650
                    )
                ),

            "disease_status":
                random.choices(
                    [
                        "ACTIVE",
                        "RECOVERED",
                        "CONTROLLED"
                    ],
                    weights=[
                        40,
                        30,
                        30
                    ]
                )[0],

            "remarks":
                random.choice([
                    "Under treatment",
                    "Routine follow-up",
                    "Stable",
                    "Recovered"
                ])
        })

    return pd.DataFrame(records)