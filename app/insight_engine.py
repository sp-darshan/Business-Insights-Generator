def generate_summary(kpis, forecast):

    summary_points = []

    # Revenue health
    if forecast["trend"] == "increasing":
        summary_points.append("Revenue is showing an upward growth trend.")
    else:
        summary_points.append("Revenue appears to be declining in upcoming months.")

    # Customer base
    if kpis["unique_customers"] > 3000:
        summary_points.append("Customer base is strong and diversified.")
    else:
        summary_points.append("Customer base is relatively small.")

    # Market dependency
    summary_points.append(
        f"Major revenue contribution comes from {kpis['top_country']}."
    )

    # Business health score (simple logic)
    score = 70
    if forecast["trend"] == "increasing":
        score += 10
    if kpis["unique_customers"] > 3000:
        score += 10

    score = min(score, 100)

    return {
        "summary": " ".join(summary_points),
        "business_health_score": score
    }
