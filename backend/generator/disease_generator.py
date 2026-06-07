import pandas as pd


def generate_diseases():

    diseases = [

        ("Diabetes", "CHRONIC"),
        ("Hypertension", "CHRONIC"),
        ("Asthma", "CHRONIC"),
        ("Tuberculosis", "INFECTIOUS"),
        ("Anemia", "NUTRITIONAL"),
        ("Malaria", "INFECTIOUS"),
        ("Dengue", "INFECTIOUS"),
        ("Pneumonia", "RESPIRATORY"),
        ("COPD", "RESPIRATORY"),
        ("Arthritis", "CHRONIC"),

        ("Typhoid", "INFECTIOUS"),
        ("Hepatitis B", "INFECTIOUS"),
        ("Hepatitis C", "INFECTIOUS"),
        ("Migraine", "NEUROLOGICAL"),
        ("Epilepsy", "NEUROLOGICAL"),

        ("Heart Disease", "CARDIOVASCULAR"),
        ("Stroke", "CARDIOVASCULAR"),
        ("Kidney Disease", "CHRONIC"),
        ("Liver Disease", "CHRONIC"),
        ("Obesity", "METABOLIC"),

        ("Hypothyroidism", "ENDOCRINE"),
        ("Hyperthyroidism", "ENDOCRINE"),
        ("Depression", "MENTAL_HEALTH"),
        ("Anxiety", "MENTAL_HEALTH"),
        ("Skin Infection", "INFECTIOUS"),

        ("Chickenpox", "INFECTIOUS"),
        ("Measles", "INFECTIOUS"),
        ("COVID-19", "INFECTIOUS"),
        ("Iron Deficiency", "NUTRITIONAL"),
        ("Vitamin D Deficiency", "NUTRITIONAL")
    ]

    rows = []

    for i, (name, category) in enumerate(
        diseases,
        start=1
    ):
        rows.append({
            "disease_id": i,
            "disease_name": name,
            "disease_category": category
        })

    return pd.DataFrame(rows)