def generate_recommendations(
    forecast,
    risk_analysis,
    monte_carlo,
    health_score
):

    recommendations = []

    if forecast.get("trend") == "decreasing":
        recommendations.append("Investigate declining revenue trend and improve demand strategy.")

    anomaly_cnt = risk_analysis.get("anomaly_count", 0)
    try:
        anomaly_cnt = int(anomaly_cnt) if anomaly_cnt else 0
    except (ValueError, TypeError):
        anomaly_cnt = 0
    
    if anomaly_cnt > 10:
        recommendations.append("High anomaly frequency detected. Strengthen operational monitoring.")

    prob_dec = monte_carlo.get("probability_of_decline", 0)
    try:
        prob_dec = float(prob_dec) if prob_dec else 0
    except (ValueError, TypeError):
        prob_dec = 0
    
    if prob_dec > 0.5:
        recommendations.append("Revenue risk is elevated. Build financial contingency reserves.")

    # Extract overall score if health_score is a dict, else use it as is
    health_score_value = health_score.get("overall_score", 0) if isinstance(health_score, dict) else health_score
    try:
        health_score_value = float(health_score_value) if health_score_value else 0
    except (ValueError, TypeError):
        health_score_value = 0
        
    if health_score_value < 60:
        recommendations.append("Overall business health is weak. Strategic intervention required.")

    if not recommendations:
        recommendations.append("Business outlook is stable with moderate risk exposure.")

    return recommendations