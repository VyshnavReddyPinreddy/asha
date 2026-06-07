import pandas as pd


def generate_vaccines():

    vaccines = [
        "BCG",
        "OPV",
        "Hepatitis B",
        "Pentavalent",
        "Rotavirus",
        "PCV",
        "IPV",
        "MR",
        "JE",
        "DPT Booster",
        "Td",
        "COVID-19",
        "Influenza",
        "HPV",
        "Typhoid"
    ]

    rows = []

    for i, vaccine in enumerate(
        vaccines,
        start=1
    ):
        rows.append({
            "vaccine_id": i,
            "vaccine_name": vaccine
        })

    return pd.DataFrame(rows)