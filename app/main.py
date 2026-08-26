from fastapi import FastAPI
from app.models.transaction import Transaction
from app.services.risk_engine import calculate_risk
from app.services.database import create_table, save_transaction, get_transactions

app = FastAPI(title="Fraud Risk Manager")


create_table()


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
        "amount": transaction.amount,
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