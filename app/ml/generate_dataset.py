import pandas as pd
import random

random.seed(42)

data = []


# --------------------------------
# NORMAL TRANSACTIONS
# --------------------------------

for i in range(1000):

    amount = random.randint(100, 60000)

    location_changed = random.choice([0, 0, 0, 0, 1])

    new_device = random.choice([0, 0, 0, 0, 1])

    failed_attempts = random.choice([0, 0, 0, 1, 1, 2, 3])

    velocity = random.randint(0, 4)

    data.append({
        "amount": amount,
        "location_changed": location_changed,
        "new_device": new_device,
        "failed_attempts": failed_attempts,
        "velocity": velocity,
        "fraud": 0
    })


# --------------------------------
# FRAUD TRANSACTIONS
# --------------------------------

for i in range(1000):

    amount = random.randint(500, 150000)

    location_changed = random.choice([0, 1, 1, 1])

    new_device = random.choice([0, 1, 1, 1])

    failed_attempts = random.randint(0, 7)

    velocity = random.randint(0, 8)

    data.append({
        "amount": amount,
        "location_changed": location_changed,
        "new_device": new_device,
        "failed_attempts": failed_attempts,
        "velocity": velocity,
        "fraud": 1
    })


# --------------------------------
# CREATE DATASET
# --------------------------------

df = pd.DataFrame(data)


# Shuffle

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# Save

df.to_csv(
    "app/ml/fraud_dataset.csv",
    index=False
)


print("Dataset created successfully!")
print()
print("Total transactions:", len(df))
print()
print("Normal transactions:", len(df[df["fraud"] == 0]))
print("Fraud transactions:", len(df[df["fraud"] == 1]))
print()
print("Dataset saved to:")
print("app/ml/fraud_dataset.csv")