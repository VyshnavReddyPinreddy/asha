import pandas as pd


def generate_vaccine_schedule():

    rows = [

        (1, 0, 30, 1),      # BCG
        (2, 0, 30, 1),      # OPV
        (3, 0, 30, 1),      # Hep B

        (4, 42, 60, 1),
        (4, 70, 90, 2),
        (4, 98, 120, 3),

        (5, 42, 60, 1),
        (5, 70, 90, 2),

        (6, 42, 60, 1),
        (6, 98, 120, 2),

        (7, 98, 120, 1),

        (8, 270, 365, 1),
        (8, 450, 550, 2),

        (9, 270, 365, 1),

        (10, 540, 730, 1),
        (10, 1800, 2200, 2),

        (11, 3650, 5000, 1),

        (12, 4380, 30000, 1),

        (13, 3650, 30000, 1),

        (14, 3285, 5475, 1),

        (15, 730, 5475, 1)
    ]

    result = []

    for schedule_id, row in enumerate(
        rows,
        start=1
    ):

        result.append({

            "schedule_id":
                schedule_id,

            "vaccine_id":
                row[0],

            "minimum_age_days":
                row[1],

            "maximum_age_days":
                row[2],

            "dose_number":
                row[3]
        })

    return pd.DataFrame(result)