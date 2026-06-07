import pandas as pd
import random
from datetime import timedelta


def generate_anc_visits(pregnancy_df):

    visits = []

    visit_id = 1

    for _, pregnancy in pregnancy_df.iterrows():

        num_visits = random.choices(
            [1, 2, 3, 4, 5, 6],
            weights=[5, 10, 15, 40, 20, 10]
        )[0]

        lmp_date = pd.to_datetime(
            pregnancy["lmp_date"]
        )

        for visit_num in range(num_visits):

            visit_date = (
                lmp_date +
                timedelta(
                    days=(visit_num + 1) * 30
                )
            )

            visits.append({

                "visit_id": visit_id,

                "pregnancy_id":
                    pregnancy["pregnancy_id"],

                "visit_date":
                    visit_date.date(),

                "weight_kg":
                    round(
                        random.uniform(45, 85),
                        1
                    ),

                "blood_pressure":
                    random.choice([
                        "110/70",
                        "120/80",
                        "130/85",
                        "140/90"
                    ]),

                "hemoglobin_level":
                    round(
                        random.uniform(8, 15),
                        1
                    ),

                "remarks":
                    random.choice([
                        "Normal",
                        "Follow-up required",
                        "Iron supplements advised",
                        "Healthy pregnancy"
                    ])
            })

            visit_id += 1

    return pd.DataFrame(visits)