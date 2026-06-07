# newborn_generator.py

import pandas as pd
import random


def generate_newborns(person_df, pregnancy_df):

    completed = pregnancy_df[
        pregnancy_df["pregnancy_status"] == "COMPLETED"
    ]

    next_person_id = (
        person_df["person_id"].max() + 1
    )

    newborns = []

    for _, preg in completed.iterrows():

        mother = person_df[
            person_df["person_id"]
            ==
            preg["mother_id"]
        ].iloc[0]

        newborns.append({

            "person_id": next_person_id,

            "first_name":
                f"Baby{next_person_id}",

            "last_name":
                mother["last_name"],

            "date_of_birth":
                preg["expected_delivery_date"],

            "gender":
                random.choice(["M", "F"]),

            "phone_number":
                None,

            "blood_group":
                random.choice([
                    "A+","A-",
                    "B+","B-",
                    "AB+","AB-",
                    "O+","O-"
                ]),

            "marital_status":
                "SINGLE",

            "status":
                "ALIVE",

            "family_id":
                mother["family_id"],

            "father_id":
                preg["father_id"],

            "mother_id":
                preg["mother_id"]
        })

        next_person_id += 1

    return pd.DataFrame(newborns)