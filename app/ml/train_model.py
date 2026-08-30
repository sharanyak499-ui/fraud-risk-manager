import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------
# LOAD DATASET
# --------------------------------

df = pd.read_csv("app/ml/fraud_dataset.csv")


# --------------------------------
# FEATURES AND TARGET
# --------------------------------

X = df[
    [
        "amount",
        "location_changed",
        "new_device",
        "failed_attempts",
        "velocity"
    ]
]

y = df["fraud"]


# --------------------------------
# TRAIN / TEST SPLIT
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------
# CREATE MODEL
# --------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# --------------------------------
# TRAIN MODEL
# --------------------------------

model.fit(X_train, y_train)


# --------------------------------
# TEST MODEL
# --------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("Model trained successfully!")

print()
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print()
print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print()
print("Classification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# --------------------------------
# SAVE MODEL
# --------------------------------

joblib.dump(
    model,
    "app/ml/fraud_model.pkl"
)


print()
print("Model saved to:")
print("app/ml/fraud_model.pkl")