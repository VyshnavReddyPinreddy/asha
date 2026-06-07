import pandas as pd
import random


def generate_vaccination_records(
    person_df,
    schedule_df
):

    person_df = person_df.copy()

    person_df["date_of_birth"] = pd.to_datetime(
        person_df["date_of_birth"]
    )

    today = pd.Timestamp.today()

    person_df["age_days"] = (
        today - person_df["date_of_birth"]
    ).dt.days

    records = []

    vaccination_id = 1

    for _, schedule in schedule_df.iterrows():

        eligible = person_df[

            (person_df["age_days"]
             >= schedule["minimum_age_days"])

            &

            (person_df["age_days"]
             <= schedule["maximum_age_days"])

        ]

        if eligible.empty:
            continue

        # Not everyone gets vaccinated

        sample_size = int(
            len(eligible) * 0.70
        )

        sample_size = min(
            sample_size,
            len(eligible)
        )

        vaccinated = eligible.sample(
            n=sample_size,
            random_state=42
        )

        for _, person in vaccinated.iterrows():

            records.append({

                "vaccination_id":
                    vaccination_id,

                "person_id":
                    int(
                        person["person_id"]
                    ),

                "schedule_id":
                    int(
                        schedule["schedule_id"]
                    ),

                "vaccination_date":
                    (
                        person["date_of_birth"]
                        +
                        pd.Timedelta(
                            days=random.randint(
                                int(
                                    schedule[
                                        "minimum_age_days"
                                    ]
                                ),
                                int(
                                    schedule[
                                        "maximum_age_days"
                                    ]
                                )
                            )
                        )
                    ).date()
            })

            vaccination_id += 1

    return pd.DataFrame(records)