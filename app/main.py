from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.models.transaction import Transaction

from app.services.risk_engine import calculate_risk

from app.services.database import (
    create_table,
    save_transaction,
    get_transactions,
    get_transaction_by_id,
    transaction_exists,
    get_user_transaction_velocity,
    get_user_average_amount
)

from app.ml.model_info import get_model_info


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Fraud Risk Manager"
)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "loaded",
        "database": "connected"
    }


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# ==========================================
# CREATE DATABASE TABLE
# ==========================================

create_table()


# ==========================================
# DASHBOARD
# ==========================================

@app.get("/", response_class=HTMLResponse)
def dashboard():

    with open(
        "app/static/index.html",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ==========================================
# CHECK TRANSACTION RISK
# ==========================================

@app.post("/check-risk")
def check_risk(transaction: Transaction):

    # --------------------------------------
    # 1. CHECK DUPLICATE TRANSACTION
    # --------------------------------------

    if transaction_exists(
        transaction.transaction_id
    ):

        raise HTTPException(
            status_code=409,
            detail={
                "error": "Transaction ID already exists",
                "transaction_id": transaction.transaction_id
            }
        )

    # --------------------------------------
    # 2. CALCULATE USER TRANSACTION VELOCITY
    # --------------------------------------

    velocity = (
        get_user_transaction_velocity(
            transaction.user_id,
            5
        ) + 1
    )

    # --------------------------------------
    # 3. GET USER AVERAGE AMOUNT
    # --------------------------------------

    user_average_amount = get_user_average_amount(
        transaction.user_id
    )

    # --------------------------------------
    # 4. CALCULATE FINAL RISK
    # --------------------------------------

    (
        score,
        level,
        decision,
        reasons,
        ml_result,
        ml_confidence,
        fraud_probability
    ) = calculate_risk(
        transaction.amount,
        transaction.location_changed,
        transaction.new_device,
        transaction.failed_attempts,
        velocity,
        user_average_amount
    )

    # --------------------------------------
    # 5. CREATE RESULT
    # --------------------------------------

    result = {
        "transaction_id": transaction.transaction_id,
        "user_id": transaction.user_id,
        "amount": transaction.amount,
        "risk_score": score,
        "risk_level": level,
        "decision": decision,
        "reasons": reasons,
        "ml_result": ml_result,
        "ml_probability": fraud_probability
    }

    # --------------------------------------
    # 6. SAVE TRANSACTION
    # --------------------------------------

    save_transaction(result)

    # --------------------------------------
    # 7. RETURN RESULT
    # --------------------------------------

    return result


# ==========================================
# GET TRANSACTION HISTORY
# ==========================================

@app.get("/transactions")
def transactions():

    return get_transactions()


# ==========================================
# GET TRANSACTION DETAILS
# ==========================================

@app.get("/transactions/{transaction_id}")
def transaction_details(transaction_id):

    result = get_transaction_by_id(
        transaction_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Transaction not found",
                "transaction_id": transaction_id
            }
        )

    return result


# ==========================================
# ML MODEL INFORMATION
# ==========================================

@app.get("/model-info")
def model_info():

    return get_model_info()