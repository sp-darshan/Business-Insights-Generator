def compute_health_score(
    forecast,
    risk_analysis,
    monte_carlo,
    kpis
):
    score = 100

    # --------------------------
    # 1️⃣ Forecast Trend Impact
    # --------------------------
    if forecast["trend"] == "decreasing":
        score -= 20
    else:
        score += 5

    # --------------------------
    # 2️⃣ Forecast Accuracy Penalty
    # --------------------------
    mape = forecast["evaluation"]["mape"]
    if mape > 50:
        score -= 20
    elif mape > 30:
        score -= 10

    # --------------------------
    # 3️⃣ Anomaly Risk Penalty
    # --------------------------
    anomaly_count = risk_analysis["anomaly_count"]

    if anomaly_count > 15:
        score -= 20
    elif anomaly_count > 5:
        score -= 10

    # --------------------------
    # 4️⃣ Monte Carlo Risk
    # --------------------------
    prob_decline = monte_carlo["probability_of_decline"]

    if prob_decline > 0.6:
        score -= 20
    elif prob_decline > 0.4:
        score -= 10

    # --------------------------
    # 5️⃣ Revenue Concentration Risk
    # --------------------------
    if kpis["top_country"] == "United Kingdom":
        score -= 5   # small dependency penalty

    # Normalize bounds
    score = max(0, min(100, score))

    return score