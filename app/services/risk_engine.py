def calculate_risk(amount, location_changed, new_device, failed_attempts):
    score = 0
    reasons = []

    if amount > 50000:
        score += 30
        reasons.append("High transaction amount")

    if location_changed:
        score += 25
        reasons.append("Location changed")

    if new_device:
        score += 20
        reasons.append("New device detected")

    if failed_attempts >= 3:
        score += 25
        reasons.append("Multiple failed attempts")

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level, reasons