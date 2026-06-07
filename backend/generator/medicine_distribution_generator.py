import pandas as pd
import random


def generate_medicine_distribution(
    person_df,
    num_records=200000
):

    rows = []

    person_ids = (
        person_df["person_id"]
        .tolist()
    )

    for distribution_id in range(
        1,
        num_records + 1
    ):

        rows.append({

            "distribution_id":
                distribution_id,

            "person_id":
                random.choice(
                    person_ids
                ),

            "medicine_id":
                random.randint(
                    1,
                    40
                ),

            "quantity":
                random.randint(
                    1,
                    30
                ),

            "distribution_date":
                (
                    pd.Timestamp.today()
                    -
                    pd.Timedelta(
                        days=random.randint(
                            0,
                            3650
                        )
                    )
                ).date()
        })

    return pd.DataFrame(rows)