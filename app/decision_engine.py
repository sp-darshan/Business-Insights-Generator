def generate_recommendations(
    forecast,
    risk_analysis,
    monte_carlo,
    health_score
):

    recommendations = []

    if forecast["trend"] == "decreasing":
        recommendations.append("Investigate declining revenue trend and improve demand strategy.")

    if risk_analysis["anomaly_count"] > 10:
        recommendations.append("High anomaly frequency detected. Strengthen operational monitoring.")

    if monte_carlo["probability_of_decline"] > 0.5:
        recommendations.append("Revenue risk is elevated. Build financial contingency reserves.")

    if health_score < 60:
        recommendations.append("Overall business health is weak. Strategic intervention required.")

    if not recommendations:
        recommendations.append("Business outlook is stable with moderate risk exposure.")

    return recommendations