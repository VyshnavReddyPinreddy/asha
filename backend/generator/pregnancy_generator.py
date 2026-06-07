import pandas as pd
import random
from datetime import timedelta


def generate_pregnancies(person_df, count=20000):

    person_df = person_df.copy()

    person_df["date_of_birth"] = pd.to_datetime(
        person_df["date_of_birth"]
    )

    today = pd.Timestamp.today()

    person_df["age"] = (
        (today - person_df["date_of_birth"]).dt.days // 365
    )

    # Eligible mothers
    eligible_mothers = person_df[
        (person_df["gender"] == "F") &
        (person_df["age"] >= 18) &
        (person_df["age"] <= 45)
    ]

    print(
        f"Eligible mothers: {len(eligible_mothers)}"
    )

    selected_mothers = eligible_mothers.sample(
        n=count,
        replace=False,
        random_state=42
    )

    # Build father lookup ONCE
    adult_males = person_df[
        (person_df["gender"] == "M") &
        (person_df["age"] >= 18)
    ]

    family_fathers = (
        adult_males
        .groupby("family_id")["person_id"]
        .first()
        .to_dict()
    )

    pregnancies = []

    for pregnancy_id, (_, mother) in enumerate(
        selected_mothers.iterrows(),
        start=1
    ):

        family_id = mother["family_id"]

        father_id = family_fathers.get(
            family_id,
            None
        )

        lmp_date = (
            today -
            timedelta(days=random.randint(0, 280))
        )

        pregnancy_status = random.choices(
            ["ONGOING", "COMPLETED", "ABORTED"],
            weights=[20, 75, 5]
        )[0]

        risk_category = random.choices(
            ["NORMAL", "HIGH_RISK"],
            weights=[85, 15]
        )[0]

        pregnancies.append({

            "pregnancy_id": pregnancy_id,

            "mother_id":
                int(mother["person_id"]),

            "father_id":
                int(father_id)
                if father_id is not None
                else None,

            "lmp_date":
                lmp_date.date(),

            "expected_delivery_date":
                (lmp_date + timedelta(days=280)).date(),

            "pregnancy_status":
                pregnancy_status,

            "risk_category":
                risk_category
        })

    return pd.DataFrame(pregnancies)