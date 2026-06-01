def predict_health(glucose, haemoglobin, cholesterol):

    score = 0

    if glucose > 180:
        score += 2
    elif glucose > 140:
        score += 1

    if cholesterol > 240:
        score += 2
    elif cholesterol > 200:
        score += 1

    if haemoglobin < 10:
        score += 1

    if score >= 4:
        return "High Risk - Consult a Doctor"

    elif score >= 2:
        return "Moderate Risk - Monitor Health"

    else:
        return "Low Risk - Healthy"