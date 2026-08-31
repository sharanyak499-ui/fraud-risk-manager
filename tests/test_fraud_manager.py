from fastapi.testclient import TestClient

from app.main import app
from app.services.risk_engine import calculate_risk


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model"] == "loaded"
    assert data["database"] == "connected"


def test_low_risk_transaction():
    score, level, decision, reasons, ml_result, confidence, probability = calculate_risk(
        2000,
        False,
        False,
        0,
        0,
        0
    )

    assert score == 0
    assert level == "LOW"
    assert decision == "APPROVE"


def test_medium_risk_transaction():
    score, level, decision, reasons, ml_result, confidence, probability = calculate_risk(
        30000,
        True,
        False,
        0,
        0,
        0
    )

    assert score >= 40
    assert level == "MEDIUM"
    assert decision == "REVIEW"


def test_high_risk_transaction():
    score, level, decision, reasons, ml_result, confidence, probability = calculate_risk(
        150000,
        True,
        True,
        5,
        0,
        0
    )

    assert score == 100
    assert level == "HIGH"
    assert decision == "BLOCK"


def test_model_info():
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "Random Forest Classifier"
    assert "feature_importance" in data


def test_transaction_history_endpoint():
    response = client.get("/transactions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)