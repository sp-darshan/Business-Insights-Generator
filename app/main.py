from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.data_preprocessor import load_and_clean_data, get_monthly_revenue, get_daily_revenue
from app.data_preprocessor_dynamic import (
    load_and_clean_data_dynamic,
    get_monthly_revenue,
    get_daily_revenue,
    get_dataset_info
)
from app.kpi_engine import calculate_kpis
from app.arima_model import forecast_revenue
from app.insight_engine import generate_summary
from app.autoencoder import detect_anomalies
from app.vae import generate_scenarios
from app.gan_model import generate_synthetic_data
from app.monte_carlo import monte_carlo_simulation
from fastapi import Body
from app.simulation_engine import run_what_if_analysis
from app.health_score import compute_health_score
from app.decision_engine import generate_recommendations
from app.prompt_builder import build_executive_prompt
from app.transformer_reasoning import generate_ai_summary
import matplotlib.pyplot as plt
import json
import tempfile
import os


app = FastAPI(title="Business Insights Generator", version="2.0")

@app.get("/generate-insights")
def generate_insights():

    df = load_and_clean_data("data/online_retail.csv")
    print(df.head())

    monthly_revenue = get_monthly_revenue(df)

    kpis = calculate_kpis(df)

    forecast = forecast_revenue(monthly_revenue)
    monte_carlo = monte_carlo_simulation(monthly_revenue, forecast)
    
    summary = generate_summary(kpis, forecast)

    daily_revenue = get_daily_revenue(df)
    risk_analysis = detect_anomalies(daily_revenue)
    health_score = compute_health_score(
        forecast,
        risk_analysis,
        monte_carlo,
        kpis
    )

    recommendations = generate_recommendations(
        forecast,
        risk_analysis,
        monte_carlo,
        health_score
    )

    scenarios = generate_scenarios(monthly_revenue)
    synthetic_data_full = generate_synthetic_data(monthly_revenue)
    # Store training history but don't expose it in API
    synthetic_data = synthetic_data_full.get("synthetic_revenue_samples", [])

    prompt = build_executive_prompt(
        kpis,
        forecast,
        risk_analysis,
        monte_carlo,
        health_score
    )

    try:
        ai_summary = generate_ai_summary(prompt)
    except Exception:
        ai_summary = "AI reasoning temporarily unavailable."

    return {
        "kpis": kpis,
        "forecast": forecast,
        "risk_analysis": risk_analysis,
        "scenarios": scenarios,
        "synthetic_data": synthetic_data,
        "monte_carlo": monte_carlo,
        "health_score": health_score,
        "recommendations": recommendations,
        "insights": summary,
        "ai_executive_summary": ai_summary,
        "meta": {
            "model": "Hybrid GenAI Business Engine v5.0"
        }
    }

@app.post("/what-if")
def what_if_analysis(
    country: str = Body(None),
    revenue_change_percent: float = Body(0)
):

    df = load_and_clean_data("data/online_retail.csv")

    result = run_what_if_analysis(
        df,
        country=country,
        revenue_change_percent=revenue_change_percent
    )

    return result


# ==================== DYNAMIC DATASET ENDPOINTS ====================

@app.post("/validate-columns")
def validate_columns(file: UploadFile = File(...), column_mapping: str = Form(...)):
    """Validate if column mapping is correct"""
    try:
        mapping = json.loads(column_mapping)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = file.file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Try to load with given mapping
            df = load_and_clean_data_dynamic(tmp_path, mapping)
            info = get_dataset_info(df)
            
            return {
                "status": "success",
                "columns": list(df.columns),
                "dataset_info": info,
                "preview": df.head().to_dict(orient='records')
            }
        finally:
            os.unlink(tmp_path)
            
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )


@app.post("/analyze-dynamic")
def analyze_dynamic(
    file: UploadFile = File(...),
    column_mapping: str = Form(...),
    date_format: str = Form(None)
):
    """Analyze a dynamic dataset with column mapping"""
    try:
        mapping = json.loads(column_mapping)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = file.file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            df = load_and_clean_data_dynamic(tmp_path, mapping, date_format)
            
            monthly_revenue = get_monthly_revenue(df)
            
            kpis = calculate_kpis(df)
            
            forecast = forecast_revenue(monthly_revenue)
            monte_carlo = monte_carlo_simulation(monthly_revenue, forecast)
            
            summary = generate_summary(kpis, forecast)
            
            daily_revenue = get_daily_revenue(df)
            risk_analysis = detect_anomalies(daily_revenue)
            health_score = compute_health_score(
                forecast,
                risk_analysis,
                monte_carlo,
                kpis
            )
            
            recommendations = generate_recommendations(
                forecast,
                risk_analysis,
                monte_carlo,
                health_score
            )
            
            scenarios = generate_scenarios(monthly_revenue)
            synthetic_data_full = generate_synthetic_data(monthly_revenue)
            synthetic_data = synthetic_data_full.get("synthetic_revenue_samples", [])
            
            prompt = build_executive_prompt(
                kpis,
                forecast,
                risk_analysis,
                monte_carlo,
                health_score
            )
            
            try:
                ai_summary = generate_ai_summary(prompt)
            except Exception:
                ai_summary = "AI reasoning temporarily unavailable."
            
            dataset_info = get_dataset_info(df)
            
            return {
                "kpis": kpis,
                "forecast": forecast,
                "risk_analysis": risk_analysis,
                "scenarios": scenarios,
                "synthetic_data": synthetic_data,
                "monte_carlo": monte_carlo,
                "health_score": health_score,
                "recommendations": recommendations,
                "insights": summary,
                "ai_executive_summary": ai_summary,
                "dataset_info": dataset_info,
                "meta": {
                    "model": "Hybrid GenAI Business Engine v5.0",
                    "version": "2.0",
                    "dynamic": True
                }
            }
        finally:
            os.unlink(tmp_path)
            
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )


@app.post("/what-if-dynamic")
def what_if_dynamic(
    file: UploadFile = File(...),
    column_mapping: str = Form(...),
    metric_change_percent: float = Form(0),
    filter_column: str = Form(None),
    filter_value: str = Form(None),
    date_format: str = Form(None)
):
    """What-if analysis on dynamic dataset"""
    try:
        mapping = json.loads(column_mapping)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = file.file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            df = load_and_clean_data_dynamic(tmp_path, mapping, date_format)
            
            # Apply filter if provided
            if filter_column and filter_value:
                df = df[df[filter_column].astype(str) == filter_value]
            
            # Apply metric change
            if metric_change_percent != 0:
                change_factor = 1 + (metric_change_percent / 100)
                df['Amount'] = df['Amount'] * change_factor
            
            monthly_revenue = get_monthly_revenue(df)
            forecast = forecast_revenue(monthly_revenue)
            monte_carlo = monte_carlo_simulation(monthly_revenue, forecast)
            
            return {
                "status": "success",
                "forecast": forecast,
                "monte_carlo": monte_carlo,
                "metric_change_percent": metric_change_percent,
                "affected_records": len(df)
            }
        finally:
            os.unlink(tmp_path)
            
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )

