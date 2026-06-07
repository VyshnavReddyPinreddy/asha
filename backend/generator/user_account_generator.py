import pandas as pd


def generate_user_accounts():

    accounts = []

    user_id = 1

    # ASHA Accounts
    for asha_id in range(1, 501):

        accounts.append({

            "user_id": user_id,

            "username":
                f"asha{asha_id:04d}",

            "password_hash":
                "$2b$12$dummy_hash",

            "email":
                f"asha{asha_id:04d}@asha.gov.in",

            "role":
                "ASHA",

            "asha_id":
                asha_id,

            "anm_id":
                None
        })

        user_id += 1

    # ANM Accounts
    for anm_id in range(1, 101):

        accounts.append({

            "user_id": user_id,

            "username":
                f"anm{anm_id:04d}",

            "password_hash":
                "$2b$12$dummy_hash",

            "email":
                f"anm{anm_id:04d}@anm.gov.in",

            "role":
                "ANM",

            "asha_id":
                None,

            "anm_id":
                anm_id
        })

        user_id += 1

    # ADMIN
    accounts.append({

        "user_id":
            user_id,

        "username":
            "admin",

        "password_hash":
            "$2b$12$dummy_hash",

        "email":
            "admin@asha.gov.in",

        "role":
            "ADMIN",

        "asha_id":
            None,

        "anm_id":
            None
    })

    df = pd.DataFrame(accounts)

    df["asha_id"] = df["asha_id"].astype("Int64")
    df["anm_id"] = df["anm_id"].astype("Int64")

    return df