import pandas as pd


def generate_medicines():

    medicines = [

        ("Paracetamol", "TABLET"),
        ("Iron Folic Acid", "TABLET"),
        ("ORS", "POWDER"),
        ("Vitamin A", "SYRUP"),
        ("Amoxicillin", "CAPSULE"),

        ("Azithromycin", "TABLET"),
        ("Metformin", "TABLET"),
        ("Amlodipine", "TABLET"),
        ("Insulin", "INJECTION"),
        ("Salbutamol", "INHALER"),

        ("Calcium Tablets", "TABLET"),
        ("Zinc Tablets", "TABLET"),
        ("Albendazole", "TABLET"),
        ("Doxycycline", "TABLET"),
        ("Cetirizine", "TABLET"),

        ("ORS Sachet", "POWDER"),
        ("Pantoprazole", "TABLET"),
        ("Omeprazole", "TABLET"),
        ("Vitamin D", "CAPSULE"),
        ("Multivitamin", "TABLET"),

        ("Cough Syrup", "SYRUP"),
        ("Ibuprofen", "TABLET"),
        ("Antacid", "SYRUP"),
        ("Hydrocortisone", "CREAM"),
        ("Chloroquine", "TABLET"),

        ("Artemisinin", "TABLET"),
        ("Folic Acid", "TABLET"),
        ("Pregnancy Supplement", "TABLET"),
        ("ORS Pediatric", "POWDER"),
        ("Antiseptic Lotion", "LIQUID"),

        ("Eye Drops", "LIQUID"),
        ("Nasal Spray", "SPRAY"),
        ("Pain Relief Gel", "GEL"),
        ("Antifungal Cream", "CREAM"),
        ("Antibiotic Ointment", "CREAM"),

        ("Protein Supplement", "POWDER"),
        ("Electrolyte Powder", "POWDER"),
        ("Vitamin B Complex", "TABLET"),
        ("Calamine Lotion", "LIQUID"),
        ("Hand Sanitizer", "LIQUID")
    ]

    rows = []

    for i, med in enumerate(
        medicines,
        start=1
    ):
        rows.append({
            "medicine_id": i,
            "medicine_name": med[0],
            "medicine_type": med[1]
        })

    return pd.DataFrame(rows)