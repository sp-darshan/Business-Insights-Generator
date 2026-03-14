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
    if forecast.get("trend") == "decreasing":
        score -= 20
    else:
        score += 5

    # --------------------------
    # 2️⃣ Forecast Accuracy Penalty
    # --------------------------
    mape = forecast.get("evaluation", {}).get("mape", 0)
    try:
        mape = float(mape) if mape else 0
    except (ValueError, TypeError):
        mape = 0
    
    if mape > 50:
        score -= 20
    elif mape > 30:
        score -= 10

    # --------------------------
    # 3️⃣ Anomaly Risk Penalty
    # --------------------------
    anomaly_count = risk_analysis.get("anomaly_count", 0)
    try:
        anomaly_count = int(anomaly_count) if anomaly_count else 0
    except (ValueError, TypeError):
        anomaly_count = 0

    if anomaly_count > 15:
        score -= 20
    elif anomaly_count > 5:
        score -= 10

    # --------------------------
    # 4️⃣ Monte Carlo Risk
    # --------------------------
    prob_decline = monte_carlo.get("probability_of_decline", 0)
    try:
        prob_decline = float(prob_decline) if prob_decline else 0
    except (ValueError, TypeError):
        prob_decline = 0

    if prob_decline > 0.6:
        score -= 20
    elif prob_decline > 0.4:
        score -= 10

    # --------------------------
    # 5️⃣ Revenue Concentration Risk
    # --------------------------
    top_country = kpis.get("top_country", "")
    if top_country == "United Kingdom":
        score -= 5   # small dependency penalty

    # Normalize bounds
    overall_score = max(0, min(100, score))

    # Calculate component scores
    revenue_health = max(0, min(100, 100 - (mape if mape else 0)))
    stability_score = max(0, min(100, 100 - (anomaly_count * 5)))
    
    # Determine status
    if overall_score >= 75:
        status = "Healthy"
    elif overall_score >= 50:
        status = "At Risk"
    else:
        status = "Critical"

    return {
        "overall_score": overall_score,
        "revenue_health": revenue_health,
        "stability_score": stability_score,
        "status": status,
        "anomaly_count": anomaly_count,
        "risk_score": prob_decline * 100
    }