from fastapi import FastAPI
from app.models.transaction import Transaction
from app.services.risk_engine import calculate_risk

app = FastAPI(title="Fraud Risk Manager")


@app.get("/")
def home():
    return {"message": "Fraud Risk Manager is running"}


@app.post("/check-risk")
def check_risk(transaction: Transaction):
    score, level, decision, reasons = calculate_risk(
        transaction.amount,
        transaction.location_changed,
        transaction.new_device,
        transaction.failed_attempts
    )

    return {
        "transaction_id": transaction.transaction_id,
        "risk_score": score,
        "risk_level": level,
        "decision": decision,
        "reasons": reasons
    }