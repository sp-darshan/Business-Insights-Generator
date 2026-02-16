## 📂 Folder Structure

```
Business_Insights_Generator/
│
├── data/
│   └── online_retail.csv
│
├── app/
│   ├── main.py                   # FastAPI entry point 
│   ├── data_processor.py         # Dataset preprocessing (Time series aggregation)
│   ├── kpi_engine.py             # Calculates business KPI
│   ├── arima_model.py            # Performs time-series forecasting on monthly revenue
│   ├── autoencoder.py            # Detects anomalous revenue days
│   ├── insight_engine.py         # Converts numeric outputs into business insights
│   └── health_score.py           # Computes overall business health score based on trend
│
├── requirements.txt              # Project dependencies
└── README.md                     # Project overview and usage

```