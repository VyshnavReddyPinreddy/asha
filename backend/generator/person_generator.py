from faker import Faker
import pandas as pd
import random
from datetime import date, timedelta

fake = Faker("en_IN")


def random_dob(age_min, age_max):

    age = random.randint(age_min, age_max)

    today = date.today()

    return today - timedelta(days=age * 365)


def generate_persons(family_sizes_df):

    persons = []

    person_id = 1

    for _, row in family_sizes_df.iterrows():

        family_id = row["family_id"]
        size = row["family_size"]

        members = []

        # Father
        father_age = random.randint(25, 60)

        members.append({
            "gender": "M",
            "age": father_age,
            "marital_status": "MARRIED"
        })

        if size >= 2:

            mother_age = max(
                18,
                father_age - random.randint(-3, 8)
            )

            members.append({
                "gender": "F",
                "age": mother_age,
                "marital_status": "MARRIED"
            })

        remaining = size - len(members)

        # Children
        while remaining > 0:

            child_age = random.randint(0, 22)

            members.append({
                "gender": random.choice(["M", "F"]),
                "age": child_age,
                "marital_status": "SINGLE"
            })

            remaining -= 1

        for member in members:

            persons.append({

                "person_id": person_id,

                "first_name": fake.first_name(),

                "last_name": fake.last_name(),

                "date_of_birth": random_dob(
                    member["age"],
                    member["age"]
                ),

                "gender": member["gender"],

                "phone_number":
                    fake.msisdn()[:10]
                    if member["age"] >= 18
                    else None,

                "blood_group":
                    random.choice([
                        "A+",
                        "A-",
                        "B+",
                        "B-",
                        "AB+",
                        "AB-",
                        "O+",
                        "O-"
                    ]),

                "marital_status":
                    member["marital_status"],

                "status": "ALIVE",

                "family_id": family_id,

                "father_id": None,

                "mother_id": None
            })

            person_id += 1

    return pd.DataFrame(persons)