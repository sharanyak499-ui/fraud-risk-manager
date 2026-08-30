from app.services.ml_engine import predict_fraud


def calculate_risk(
    amount,
    location_changed,
    new_device,
    failed_attempts,
    recent_transaction_count=0,
    user_average_amount=0
):
    score = 0
    reasons = []

    # --------------------------------
    # 1. TRANSACTION AMOUNT
    # --------------------------------

    if amount > 100000:
        points = 40
        score += points
        reasons.append({
            "reason": "Very high transaction amount",
            "points": points
        })

    elif amount > 50000:
        points = 30
        score += points
        reasons.append({
            "reason": "High transaction amount",
            "points": points
        })

    elif amount > 25000:
        points = 15
        score += points
        reasons.append({
            "reason": "Unusually high transaction amount",
            "points": points
        })

    # --------------------------------
    # 2. LOCATION CHANGE
    # --------------------------------

    if location_changed:
        points = 25
        score += points
        reasons.append({
            "reason": "Location changed",
            "points": points
        })

    # --------------------------------
    # 3. NEW DEVICE
    # --------------------------------

    if new_device:
        points = 20
        score += points
        reasons.append({
            "reason": "New device detected",
            "points": points
        })

    # --------------------------------
    # 4. FAILED LOGIN ATTEMPTS
    # --------------------------------

    if failed_attempts >= 5:
        points = 35
        score += points
        reasons.append({
            "reason": "Very high number of failed attempts",
            "points": points
        })

    elif failed_attempts >= 3:
        points = 25
        score += points
        reasons.append({
            "reason": "Multiple failed attempts",
            "points": points
        })

    elif failed_attempts >= 1:
        points = 10
        score += points
        reasons.append({
            "reason": "Failed login attempt detected",
            "points": points
        })

    # --------------------------------
    # 5. TRANSACTION VELOCITY
    # --------------------------------

    if recent_transaction_count >= 5:
        points = 50
        score += points
        reasons.append({
            "reason": (
                f"Extremely high transaction frequency: "
                f"{recent_transaction_count} transactions in the last 5 minutes"
            ),
            "points": points
        })

    elif recent_transaction_count >= 4:
        points = 35
        score += points
        reasons.append({
            "reason": (
                f"Very high transaction frequency: "
                f"{recent_transaction_count} transactions in the last 5 minutes"
            ),
            "points": points
        })

    elif recent_transaction_count >= 3:
        points = 20
        score += points
        reasons.append({
            "reason": (
                f"High transaction frequency: "
                f"{recent_transaction_count} transactions in the last 5 minutes"
            ),
            "points": points
        })

    # --------------------------------
    # 6. BEHAVIORAL ANOMALY
    # --------------------------------

    if user_average_amount > 0:

        if amount >= user_average_amount * 10:
            points = 25
            score += points
            reasons.append({
                "reason": (
                    f"Transaction is unusually high compared "
                    f"with user's average of ₹{user_average_amount:.2f}"
                ),
                "points": points
            })

        elif amount >= user_average_amount * 5:
            points = 15
            score += points
            reasons.append({
                "reason": (
                    f"Transaction is significantly higher than "
                    f"user's average of ₹{user_average_amount:.2f}"
                ),
                "points": points
            })

    # --------------------------------
    # 7. MACHINE LEARNING
    # --------------------------------

    ml_result, ml_confidence, fraud_probability = predict_fraud(
    amount,
    location_changed,
    new_device,
    failed_attempts,
    recent_transaction_count
)

    if ml_result == "FRAUD":

        # ML contributes proportionally to confidence.
        ml_points = round((ml_confidence / 100) * 20)

        if ml_points > 0:
            score += ml_points

            reasons.append({
                "reason": (
                    f"ML model detected potential fraud "
                    f"({ml_confidence}% confidence)"
                ),
                "points": ml_points
            })

        # --------------------------------
        # HIGH-CONFIDENCE ML OVERRIDE
        # --------------------------------

        if ml_confidence >= 90:
            score = max(score, 80)

        elif ml_confidence >= 70:
            score = max(score, 70)

    # --------------------------------
    # 8. LIMIT SCORE
    # --------------------------------

    score = min(max(score, 0), 100)

    # --------------------------------
    # 9. RISK LEVEL + DECISION
    # --------------------------------

    if score >= 70:
        level = "HIGH"
        decision = "BLOCK"

    elif score >= 40:
        level = "MEDIUM"
        decision = "REVIEW"

    else:
        level = "LOW"
        decision = "APPROVE"

    # --------------------------------
    # 10. NO RISK FACTORS
    # --------------------------------

    if not reasons:
        reasons.append({
            "reason": "No significant risk factors detected",
            "points": 0
        })

    return (
    score,
    level,
    decision,
    reasons,
    ml_result,
    ml_confidence,
    fraud_probability
)