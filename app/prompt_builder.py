def build_executive_prompt(
    kpis,
    forecast,
    risk_analysis,
    monte_carlo,
    health_score
):
    # Extract values with type safety
    total_revenue = kpis.get('total_revenue', 0)
    try:
        total_revenue = float(total_revenue) if total_revenue else 0
    except (ValueError, TypeError):
        total_revenue = 0
    
    unique_customers = kpis.get('unique_customers', 0)
    try:
        unique_customers = int(unique_customers) if unique_customers else 0
    except (ValueError, TypeError):
        unique_customers = 0
    
    top_country = str(kpis.get('top_country', 'N/A'))
    
    trend = str(forecast.get('trend', 'unknown'))
    
    mape = forecast.get('evaluation', {}).get('mape', 0)
    try:
        mape = float(mape) if mape else 0
    except (ValueError, TypeError):
        mape = 0
    
    anomaly_count = risk_analysis.get('anomaly_count', 0)
    try:
        anomaly_count = int(anomaly_count) if anomaly_count else 0
    except (ValueError, TypeError):
        anomaly_count = 0
    
    prob_decline = monte_carlo.get('probability_of_decline', 0)
    try:
        prob_decline = float(prob_decline) if prob_decline else 0
    except (ValueError, TypeError):
        prob_decline = 0
    
    volatility = monte_carlo.get('volatility_index_percent', 0)
    try:
        volatility = float(volatility) if volatility else 0
    except (ValueError, TypeError):
        volatility = 0
    
    # Extract health score value if it's a dict
    health_score_value = health_score.get("overall_score", 0) if isinstance(health_score, dict) else health_score
    try:
        health_score_value = float(health_score_value) if health_score_value else 0
    except (ValueError, TypeError):
        health_score_value = 0

    return f"""
        Analyze the following business performance data and generate a concise executive-level summary with strategic recommendations.

        Key Metrics:
        - Total Revenue: ${total_revenue:,.2f}
        - Unique Customers: {unique_customers}
        - Top Country: {top_country}

        Forecast:
        - Trend: {trend}
        - Forecast MAPE: {mape:.2f}%

        Risk:
        - Anomaly Count: {anomaly_count}
        - Probability of Revenue Decline: {prob_decline:.2f}
        - Volatility Index: {volatility:.2f}%

        Overall Health Score: {health_score_value:.1f}/100
    """