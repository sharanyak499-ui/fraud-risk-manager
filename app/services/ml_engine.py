import joblib
import os
import pandas as pd


# --------------------------------
# LOAD TRAINED MODEL
# --------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml",
    "fraud_model.pkl"
)

model = joblib.load(MODEL_PATH)


# --------------------------------
# ML FRAUD PREDICTION
# --------------------------------

def predict_fraud(
    amount,
    location_changed,
    new_device,
    failed_attempts,
    velocity
):

    features = pd.DataFrame([
        {
            "amount": amount,
            "location_changed": int(location_changed),
            "new_device": int(new_device),
            "failed_attempts": failed_attempts,
            "velocity": velocity
        }
    ])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    # Class 0 = NORMAL
    # Class 1 = FRAUD

    normal_probability = probabilities[0]
    fraud_probability = probabilities[1]

    if prediction == 1:
        result = "FRAUD"
    else:
        result = "NORMAL"

    confidence = max(normal_probability, fraud_probability)

    return (
        result,
        round(float(confidence) * 100, 2),
        round(float(fraud_probability) * 100, 2)
    )