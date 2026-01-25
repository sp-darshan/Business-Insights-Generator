## 📂 Folder Structure

```
Buisness Insights Generator/
│
├── data/
│   ├── raw/                    # Uploaded CSVs (sales, costs, churn, KPIs)
│   ├── processed/              # Cleaned & feature-engineered data
│   └── synthetic/              # Generated demo/testing data
│
├── ingestion/
│   ├── csv_loader.py           # Load CSV files
│   ├── api_loader.py           # Optional external data ingestion
│   └── validator.py            # Schema & data validation
│
├── analytics/
│   ├── kpi_engine.py           # Revenue, churn, CAC, LTV, margins
│   ├── anomaly_detection.py    # Spikes, drops, unusual behavior
│   └── trend_analysis.py       # QoQ, YoY trend decomposition
│
├── models/
│   ├── forecasting/
│   │   ├── statistical/
│   │   │   ├── arima.py
│   │   │   └── prophet.py
│   │   └── deep_learning/
│   │       └── lstm.py
│   │
│   ├── churn/
│   │   └── churn_model.py      # Churn prediction & risk scoring
│   │
│   └── cost_optimization.py    # Expense & margin optimization
│
├── scenarios/
│   ├── pricing_scenarios.py    # Price increase/decrease simulations
│   ├── cost_scenarios.py       # Cost-cutting & efficiency scenarios
│   └── growth_scenarios.py     # Growth & scale simulations
│
├── reasoning/                  # GenAI Core
│   ├── prompt_templates.py     # Structured prompts
│   ├── insight_generator.py    # Plain-English explanations
│   ├── decision_engine.py      # Actionable recommendations
│   └── risk_assessment.py      # Business risk evaluation
│
├── reports/                    # 🔑 Premium Feature
│   ├── summary_builder.py      # Executive summaries
│   ├── pdf_generator.py        # Exportable PDF reports
│   └── excel_exporter.py       # KPI & forecast exports
│
├── evaluation/
│   ├── forecast_metrics.py     # RMSE, MAPE, accuracy
│   └── decision_quality.py     # Scenario vs outcome evaluation
│
├── api/
│   ├── main.py                 # FastAPI entry point
│   └── routes/
│       ├── analyze.py          # Insights & explanations
│       └── recommend.py        # Decisions & scenarios
│
├── frontend/
│   ├── dashboard/              # KPI & forecast views
│   └── chat_interface/         # “Ask the business” AI chat
│
├── configs/
│   ├── model_config.yaml       # Model parameters
│   └── business_rules.yaml     # SME decision rules
│
├── logs/                       # System & decision logs
├── tests/                      # Unit & integration tests
│
├── requirements.txt
└── README.md

```