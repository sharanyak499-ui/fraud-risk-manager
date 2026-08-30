import joblib
import os


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "fraud_model.pkl"
)


def get_model_info():

    model = joblib.load(MODEL_PATH)

    features = [
        "amount",
        "location_changed",
        "new_device",
        "failed_attempts",
        "velocity"
    ]

    importance = model.feature_importances_

    feature_importance = {}

    for feature, value in zip(features, importance):

        feature_importance[feature] = round(
            float(value) * 100,
            2
        )

    return {
        "model": "Random Forest Classifier",
        "feature_importance": feature_importance
    }