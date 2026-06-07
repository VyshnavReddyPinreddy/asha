from faker import Faker
import pandas as pd
import random

fake = Faker("en_IN")

def generate_anms(count: int):

    rows = []

    for anm_id in range(1, count + 1):

        rows.append({
            "anm_id": anm_id,
            "employee_code": f"ANM{anm_id:04d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone_number": f"9{random.randint(100000000,999999999)}",
            "sub_center_name": f"Sub Center {anm_id}",
            "date_of_joining": fake.date_between(
                start_date="-15y",
                end_date="-1y"
            ),
            "status": random.choices(
                ["ACTIVE", "INACTIVE", "TRANSFERRED", "RETIRED"],
                weights=[85, 5, 5, 5]
            )[0]
        })

    return pd.DataFrame(rows)