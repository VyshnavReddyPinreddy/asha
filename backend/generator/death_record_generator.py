import pandas as pd
import random


def generate_death_records(
    person_df,
    num_deaths=5000
):

    person_df = person_df.copy()

    person_df["date_of_birth"] = pd.to_datetime(
        person_df["date_of_birth"]
    )

    today = pd.Timestamp.today()

    person_df["age"] = (
        (today - person_df["date_of_birth"])
        .dt.days // 365
    )

    elderly = person_df[
        person_df["age"] >= 60
    ]

    middle_age = person_df[
        (person_df["age"] >= 40)
        &
        (person_df["age"] < 60)
    ]

    young = person_df[
        person_df["age"] < 40
    ]

    elderly_count = int(
        num_deaths * 0.75
    )

    middle_count = int(
        num_deaths * 0.20
    )

    young_count = (
        num_deaths
        -
        elderly_count
        -
        middle_count
    )

    selected = pd.concat([
        elderly.sample(
            n=min(
                elderly_count,
                len(elderly)
            ),
            random_state=42
        ),
        middle_age.sample(
            n=min(
                middle_count,
                len(middle_age)
            ),
            random_state=42
        ),
        young.sample(
            n=min(
                young_count,
                len(young)
            ),
            random_state=42
        )
    ])

    records = []

    for death_id, (
        _,
        person
    ) in enumerate(
        selected.iterrows(),
        start=1
    ):

        records.append({

            "death_id":
                death_id,

            "person_id":
                int(
                    person["person_id"]
                ),

            "date_of_death":
                (
                    today
                    -
                    pd.Timedelta(
                        days=random.randint(
                            0,
                            3650
                        )
                    )
                ).date(),

            "cause_of_death":
                random.choice([
                    "Cardiac Arrest",
                    "Stroke",
                    "Respiratory Failure",
                    "Cancer",
                    "Accident",
                    "Infection",
                    "Kidney Failure"
                ])
        })

    return pd.DataFrame(records)