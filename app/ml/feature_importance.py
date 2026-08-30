import joblib


# Load trained model
model = joblib.load("app/ml/fraud_model.pkl")


# Feature names
features = [
    "amount",
    "location_changed",
    "new_device",
    "failed_attempts",
    "velocity"
]


# Get importance
importance = model.feature_importances_


print()
print("================================")
print("FRAUD MODEL FEATURE IMPORTANCE")
print("================================")
print()


# Combine and sort
results = list(zip(features, importance))

results.sort(
    key=lambda x: x[1],
    reverse=True
)


for feature, value in results:

    print(
        f"{feature}: {value * 100:.2f}%"
    )