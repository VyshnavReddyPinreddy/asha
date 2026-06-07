from faker import Faker
import pandas as pd
import random

fake = Faker("en_IN")


def generate_ashas(num_ashas: int):

    rows = []

    for asha_id in range(1, num_ashas + 1):

        rows.append({
            "asha_id": asha_id,
            "employee_code": f"ASHA{asha_id:04d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone_number": f"8{random.randint(100000000,999999999)}",
            "date_of_joining": fake.date_between(
                start_date="-15y",
                end_date="-1y"
            ),
            "status": random.choices(
                ["ACTIVE", "INACTIVE", "TRANSFERRED", "RETIRED"],
                weights=[85, 5, 5, 5]
            )[0],
            "area_id": asha_id
        })

    return pd.DataFrame(rows)