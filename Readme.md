# 📊 Business Insights Generator

> **AI-Powered Analytics Platform** - Generate comprehensive business insights from your CSV datasets using advanced machine learning models and generative AI.

## 🎯 Project Overview

Business Insights Generator is a full-stack application that transforms raw business data into actionable insights. It combines multiple ML models (ARIMA, Autoencoders, VAE, GAN, Monte Carlo) with a modern web interface to enable data-driven decision making.

**Key Capabilities:**
- 🔄 **Dynamic CSV Support** - Upload any CSV with flexible column mapping
- 📈 **Revenue Forecasting** - ARIMA-based time-series predictions
- 🔍 **Anomaly Detection** - Identify unusual patterns using Autoencoders
- 💡 **Scenario Planning** - VAE-powered what-if analysis
- 🎲 **Risk Simulation** - Monte Carlo uncertainty quantification
- 🏥 **Health Scoring** - Comprehensive business health metrics
- 🤖 **AI-Powered Insights** - Transformer-based executive summaries
- 📊 **Interactive Dashboard** - Real-time visualizations with Streamlit

---

## 📂 Folder Structure

```
business_insights_generator/
│
├── 📁 app/                                    # Backend API & ML Models
│   ├── main.py                              # FastAPI entry point (endpoints)
│   ├── data_preprocessor.py                 # Static data loading (online_retail.csv)
│   ├── data_preprocessor_dynamic.py         # Dynamic CSV loading with column mapping
│   ├── kpi_engine.py                        # KPI calculations (revenue, avg transaction, etc.)
│   ├── arima_model.py                       # Time-series forecasting
│   ├── autoencoder.py                       # Anomaly detection on daily revenue
│   ├── baseline_model.py                    # Baseline forecasting model
│   ├── vae.py                               # Variational Autoencoder for scenarios
│   ├── gan_model.py                         # Generative Adversarial Network
│   ├── monte_carlo.py                       # Risk simulation engine
│   ├── health_score.py                      # Business health scoring (0-100)
│   ├── decision_engine.py                   # AI recommendation generation
│   ├── insight_engine.py                    # Text summary generation
│   ├── prompt_builder.py                    # Executive summary prompts
│   ├── simulation_engine.py                 # What-if scenario analysis
│   ├── transformer_reasoning.py             # Transformer-based AI reasoning
│   ├── __init__.py                          # Package initialization
│   └── __pycache__/                         # Python cache
│
├── 📁 frontend/                              # Streamlit Web Application
│   ├── streamlit_app.py                     # Main UI with 5 pages
│   ├── components/                          # Reusable UI components
│   │   ├── __init__.py
│   │   └── utils.py                         # Frontend utilities
│   ├── pages/                               # Multi-page structure
│   ├── README.md                            # Frontend documentation
│   └── __pycache__/                         # Python cache
│
├── 📁 data/                                  # Datasets
│   ├── online_retail.csv                    # E-commerce transactions (Dec 2010-Dec 2011)
│   └── superstore_sales.csv                 # Retail sales data (Jan 2022-Dec 2024)
│
├── 📁 uploads/                               # Temporary file storage for uploads
│
├── 📁 .streamlit/                            # Streamlit configuration
│   └── config.toml                          # UI/theme configuration
│
├── 📄 main.py (root)                        # Application launcher
├── quick_start.py                           # Quick setup script
├── requirements.txt                         # Python dependencies
│
├── 📋 SETUP_GUIDE.md                        # Installation & configuration
├── MODELS_DETAILED_EXPLANATION.md           # ML model documentation
├── CODE_REVIEW.md                           # Code quality notes
├── DETAILED_README.md                       # Extended documentation
│
├── 🔬 Testing & Validation Scripts
│   ├── validate_generative_models.py        # Test VAE/GAN models
│   ├── validate_risk_simulation.py          # Test Monte Carlo engine
│   ├── generate_test_data.py                # Generate synthetic test data
│   ├── plot_arima_validation.py             # ARIMA performance plots
│   └── compare_models.py                    # Model comparison analysis
│
├── 📊 Visualizations
│   └── gan_loss_plot.png                    # GAN training loss visualization
│
├── 📁 .git/                                 # Version control
├── .gitignore                               # Git ignore rules
│
└── 📄 Business_Insights_Generator.docx      # Project documentation (Word)
```

---

## ✨ Features

### 1. **Dynamic Data Upload**
- Upload any CSV file with custom column mapping
- Auto-detection of date, amount, quantity, and region columns
- Support for multiple date formats (YYYY-MM-DD, DD-MM-YYYY HH:MM, etc.)
- Intelligent column name matching

### 2. **Analytics Dashboard**
- **KPIs**: Total revenue, average transaction value, success rate
- **Forecasting**: 12-month revenue predictions
- **Anomalies**: Unusual pattern detection
- **Risk Analysis**: Worst-case, best-case, volatility metrics
- **Health Score**: 0-100 business health rating

### 3. **What-If Analysis**
- Simulate revenue changes by percentage
- Filter by region or product category
- See impact on forecasts and health scores

### 4. **Advanced ML Models**
| Model | Purpose | Output |
|-------|---------|--------|
| **ARIMA** | Time-series forecasting | 12-month revenue forecast |
| **Autoencoder** | Anomaly detection | Daily anomaly flags |
| **VAE** | Scenario generation | Alternative business scenarios |
| **GAN** | Synthetic data | Synthetic revenue patterns |
| **Monte Carlo** | Risk simulation | Confidence intervals & volatility |

### 5. **AI-Powered Insights**
- Executive summaries using transformers
- Automated recommendations
- Business metric interpretation

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- pip package manager

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- FastAPI & Uvicorn (backend API)
- Streamlit (frontend UI)
- pandas, numpy (data processing)
- scikit-learn (ML models)
- TensorFlow/Keras (deep learning)
- matplotlib, plotly (visualization)

### Step 2: Start FastAPI Backend

```bash
python app/main.py
# or
uvicorn app.main:app --reload --port 8000
```

**Backend runs at:** `http://localhost:8000`

### Step 3: Start Streamlit Frontend

```bash
streamlit run frontend/streamlit_app.py
# or
python -m streamlit run frontend/streamlit_app.py
```

**Frontend runs at:** `http://localhost:8501`

### Quick Start (All-in-One)

```bash
python quick_start.py
```

---

## 📖 Usage Guide

### **Page 1: Home**
- Overview of features
- Model statistics
- Quick start instructions

### **Page 2: Upload Dataset**
- Download test dataset option
- Upload your CSV file
- See data preview and requirements

### **Page 3: Configure Columns**
- Auto-detected column mapping
- Manual column selection
- Data validation metrics
- Preview of mapped data

### **Page 4: Dashboard**
- Key Performance Indicators (KPIs)
- Revenue forecast chart
- Anomaly detection results
- Monte Carlo simulation results
- Health score with breakdown
- AI-generated insights
- Recommendations

### **Page 5: What-If Analysis**
- Simulate revenue changes
- Filter by region/category
- View updated forecasts
- Compare scenarios

---

## 🔌 Backend API Endpoints

### Static Dataset (Pre-loaded)
```
GET /generate-insights
- Returns full analysis for online_retail.csv
```

### Dynamic Datasets (User Upload)
```
POST /validate-columns
- Validate CSV column mapping
- Accepts: file, column_mapping, date_format
- Returns: validation status, dataset info

POST /analyze-dynamic
- Full analysis on uploaded dataset
- Accepts: file, column_mapping, date_format
- Returns: KPIs, forecasts, anomalies, health score, recommendations

POST /what-if-dynamic
- Scenario analysis on uploaded dataset
- Accepts: file, column_mapping, metric_change_percent, filter_column, filter_value, date_format
- Returns: Updated forecasts and health score
```

---


## 🧠 ML Models Explained

### **ARIMA (Auto Regressive Integrated Moving Average)**
- **Purpose**: Time-series forecasting
- **Input**: Monthly revenue data
- **Output**: 12-month revenue forecast with confidence intervals
- **Best For**: Trending data with seasonal patterns

### **Autoencoder (Neural Network)**
- **Purpose**: Detect anomalous days
- **Input**: Daily revenue values
- **Output**: Anomaly flags with severity scores
- **Best For**: Identifying unusual business activity

### **VAE (Variational Autoencoder)**
- **Purpose**: Generate alternative business scenarios
- **Input**: Historical revenue patterns
- **Output**: Multiple scenario possibilities
- **Best For**: What-if analysis

### **GAN (Generative Adversarial Network)**
- **Purpose**: Generate synthetic realistic revenue data
- **Input**: Historical revenue distribution
- **Output**: Synthetic revenue samples
- **Best For**: Data augmentation & testing

### **Monte Carlo Simulation**
- **Purpose**: Risk and uncertainty quantification
- **Input**: Forecasted revenue with volatility
- **Output**: Confidence intervals, worst-case, best-case scenarios
- **Best For**: Risk assessment

---
