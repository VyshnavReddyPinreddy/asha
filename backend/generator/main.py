from user_account_generator import (
    generate_user_accounts
)

df = generate_user_accounts()

df.to_csv(
    "output/user_account.csv",
    index=False
)

print(len(df))