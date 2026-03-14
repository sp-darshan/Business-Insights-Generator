def generate_summary(kpis, forecast):

    summary_points = []

    # Revenue trend
    if forecast.get("trend") == "increasing":
        summary_points.append("Revenue is showing an upward growth trend.")
    else:
        summary_points.append("Revenue appears to be declining in upcoming months.")

    # Customer base
    unique_customers = kpis.get("unique_customers", 0)
    try:
        unique_customers = int(unique_customers) if unique_customers else 0
    except (ValueError, TypeError):
        unique_customers = 0
    
    if unique_customers > 3000:
        summary_points.append("Customer base is strong and diversified.")
    else:
        summary_points.append("Customer base is relatively small.")

    # Market dependency
    summary_points.append(
        f"Major revenue contribution comes from {kpis.get('top_country', 'N/A')}."
    )

    return {
        "summary": " ".join(summary_points)
    }
