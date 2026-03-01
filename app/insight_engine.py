def generate_summary(kpis, forecast):

    summary_points = []

    # Revenue trend
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

    return {
        "summary": " ".join(summary_points)
    }
