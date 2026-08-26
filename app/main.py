from fastapi import FastAPI
from app.models.transaction import Transaction
from app.services.risk_engine import calculate_risk
from app.services.transaction_store import save_transaction, get_transactions

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

    result = {
        "transaction_id": transaction.transaction_id,
        "risk_score": score,
        "risk_level": level,
        "decision": decision,
        "reasons": reasons
    }

    save_transaction(result)

    return result


@app.get("/transactions")
def transactions():
    return get_transactions()