import streamlit as st
import pandas as pd
import requests
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Business Insights Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'dataset_info' not in st.session_state:
    st.session_state.dataset_info = None

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Business Insights Generator")
st.markdown("*Unlock actionable insights from your business data using AI-powered analytics*")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Home", "Upload Dataset", "Configure Columns", "Dashboard", "What-If Analysis"],
    index=0
)

# Backend API configuration
API_BASE_URL = "http://localhost:8000"

st.sidebar.markdown("---")
st.sidebar.info(
    "**📌 How to use:**\n"
    "1. Upload your CSV dataset\n"
    "2. Map your columns to standard fields\n"
    "3. View insights on the dashboard\n"
    "4. Run what-if scenarios\n\n"
    "**ℹ️ Supported file format:** CSV only"
)

# ==================== HOME PAGE ====================
if page == "Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Welcome! 👋
        
        This application helps you generate comprehensive business insights from your data using advanced ML models:
        
        **📈 Features:**
        - **Revenue Forecasting** - ARIMA time-series predictions
        - **Anomaly Detection** - Identify unusual patterns using Autoencoders
        - **Risk Analysis** - Monte Carlo simulations for uncertainty
        - **Health Scoring** - Comprehensive business health metrics
        - **AI Insights** - Generative AI-powered recommendations
        - **What-If Analysis** - Scenario planning and testing
        """)
    
    with col2:
        st.image("https://via.placeholder.com/400x300?text=Business+Analytics", width=800)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Models", "10+")
    with col2:
        st.metric("🔍 Metrics", "50+")
    with col3:
        st.metric("⚡ Speed", "< 2min")
    
    st.markdown("---")
    st.markdown("### 🚀 Get Started")
    st.info("Navigate to **Upload Dataset** to begin analyzing your data!")

# ==================== UPLOAD DATASET PAGE ====================
elif page == "Upload Dataset":
    st.header("📁 Upload Your Dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Requirements:
        - **Format:** CSV file
        - **Date Column:** Must contain transaction/order dates
        - **Amount Column:** Must contain revenue/sales amounts
        - **Optional:** Quantity, Country/Region, Category columns
        
        ### Sample Dataset:
        You can download and use our test dataset (Superstore Sales Data)
        """)
    
    with col2:
        # Download test dataset
        if st.button("📥 Download Test Dataset", width='stretch'):
            test_data_path = Path("data/superstore_sales.csv")
            if test_data_path.exists():
                with open(test_data_path, "rb") as f:
                    st.download_button(
                        label="Download superstore_sales.csv",
                        data=f.read(),
                        file_name="superstore_sales.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("Test dataset not found. Please add it to the data/ folder.")
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file:",
        type=["csv"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # Store in session state
        st.session_state.uploaded_file = uploaded_file
        
        # Show file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Preview the file
        try:
            df = pd.read_csv(uploaded_file)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            
            st.subheader("Dataset Preview")
            st.dataframe(df.head(10), width='stretch')
            
            st.subheader("Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Non-Null': df.count(),
                'Null': df.isnull().sum()
            })
            st.dataframe(col_info, width='stretch')
            
            st.info("✨ Next: Go to **Configure Columns** to map your dataset columns")
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# ==================== CONFIGURE COLUMNS PAGE ====================
elif page == "Configure Columns":
    st.header("🔧 Configure Column Mapping")
    
    if st.session_state.uploaded_file is None:
        st.warning("⚠️ Please upload a dataset first on the 'Upload Dataset' page")
    else:
        # Read the file again to get columns
        st.session_state.uploaded_file.seek(0)
        try:
            df = pd.read_csv(st.session_state.uploaded_file, on_bad_lines='skip', engine='python')
        except Exception:
            # Fallback without engine specification
            st.session_state.uploaded_file.seek(0)
            df = pd.read_csv(st.session_state.uploaded_file, on_bad_lines='skip')
        columns = df.columns.tolist()
        
        # Smart column detection based on column names
        def find_best_match(keywords, columns, exclude=None):
            """Find the best matching column based on keywords"""
            if exclude is None:
                exclude = []
            available = [c for c in columns if c not in exclude]
            
            for keyword_set in keywords:
                for col in available:
                    col_lower = col.lower()
                    for keyword in keyword_set:
                        if keyword.lower() in col_lower:
                            return col
            return available[0] if available else None
        
        # Detect columns
        date_options = [['date', 'orderdate', 'invoicedate', 'transactiondate', 'createddate'],
                       ['day', 'time']]
        amount_options = [['amount', 'sales', 'revenue', 'total', 'price'],
                         ['salesamount', 'totalamount', 'revenue']]
        quantity_options = [['quantity', 'qty', 'count', 'units']]
        country_options = [['country', 'region', 'location', 'state', 'city']]
        
        detected_date = find_best_match(date_options, columns)
        detected_amount = find_best_match(amount_options, columns, exclude=[detected_date] if detected_date else [])
        detected_quantity = find_best_match(quantity_options, columns, exclude=[detected_date, detected_amount] if detected_date and detected_amount else [])
        detected_country = find_best_match(country_options, columns, exclude=[detected_date, detected_amount] if detected_date and detected_amount else [])
        
        # Show auto-detection info
        st.info("🤖 **Auto-Detection**: The system detected that your columns likely map as shown below. Adjust if needed.")
        
        st.markdown("""
        ### Map Your Columns
        Select which columns in your dataset correspond to these standard fields:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            date_col = st.selectbox(
                "📅 Date Column *",
                options=columns,
                index=columns.index(detected_date) if detected_date in columns else 0,
                help="Must contain transaction/order dates"
            )
            
            quantity_col = st.selectbox(
                "📦 Quantity Column (Optional)",
                options=[None] + columns,
                index=(columns.index(detected_quantity) + 1) if detected_quantity and detected_quantity in columns else 0,
                help="Number of items per transaction"
            )
        
        with col2:
            amount_col = st.selectbox(
                "💰 Amount Column *",
                options=columns,
                index=columns.index(detected_amount) if detected_amount in columns else 0,
                help="Revenue/Sales amount for each transaction"
            )
            
            country_col = st.selectbox(
                "🌍 Country/Region Column (Optional)",
                options=[None] + columns,
                index=(columns.index(detected_country) + 1) if detected_country and detected_country in columns else 0,
                help="Geographic location for filtering"
            )
        
        # Date format selector
        st.subheader("📅 Date Format")
        date_format_option = st.radio(
            "Select or specify date format:",
            ["Auto-detect", "DD-MM-YYYY", "DD-MM-YYYY HH:MM", "MM-DD-YYYY", "YYYY-MM-DD", "Custom"],
            horizontal=False,
            help="Choose the format that matches your data (e.g., '01-12-2010 08:26' = DD-MM-YYYY HH:MM)"
        )
        
        date_format = None
        if date_format_option == "Auto-detect":
            date_format = None  # Backend will auto-detect intelligently
        elif date_format_option == "DD-MM-YYYY":
            date_format = "%d-%m-%Y"
        elif date_format_option == "DD-MM-YYYY HH:MM":
            date_format = "%d-%m-%Y %H:%M"
        elif date_format_option == "MM-DD-YYYY":
            date_format = "%m-%d-%Y"
        elif date_format_option == "YYYY-MM-DD":
            date_format = "%Y-%m-%d"
        else:
            date_format = st.text_input("Enter date format (e.g., %d/%m/%Y):")
        
        # Show data preview of selected columns
        st.subheader("👀 Data Preview")
        preview_cols = [date_col, amount_col]
        if quantity_col:
            preview_cols.append(quantity_col)
        if country_col:
            preview_cols.append(country_col)
        
        preview_df = df[preview_cols].head(10)
        st.dataframe(preview_df, width='stretch', use_container_width=True)
        
        # Validate selections
        st.subheader("✅ Validation")
        val_col1, val_col2, val_col3, val_col4 = st.columns(4)
        
        try:
            with val_col1:
                date_vals = pd.to_datetime(df[date_col], errors='coerce')
                valid_dates = date_vals.notna().sum()
                st.metric("Valid Dates", f"{valid_dates}/{len(df)}")
                
            with val_col2:
                amount_vals = pd.to_numeric(df[amount_col], errors='coerce')
                valid_amounts = amount_vals.notna().sum()
                st.metric("Valid Amounts", f"{valid_amounts}/{len(df)}")
                
            with val_col3:
                total_amount = pd.to_numeric(df[amount_col], errors='coerce').sum()
                st.metric("Total Amount", f"${total_amount:,.2f}")
                
            with val_col4:
                avg_amount = pd.to_numeric(df[amount_col], errors='coerce').mean()
                st.metric("Avg Amount", f"${avg_amount:,.2f}")
        except Exception as e:
            st.warning(f"⚠️ Could not validate data: {str(e)}")
        
        # Build column mapping
        mapping = {
            "date_column": date_col,
            "amount_column": amount_col,
        }
        if quantity_col:
            mapping["quantity_column"] = quantity_col
        if country_col:
            mapping["country_column"] = country_col
        
        st.session_state.column_mapping = mapping
        
        # Validate button
        if st.button("✅ Validate & Continue", width='stretch', type="primary"):
            st.info("🔍 Validating column mapping...")
            
            # Prepare files for validation - reset file pointer and read as bytes
            st.session_state.uploaded_file.seek(0)
            file_content = st.session_state.uploaded_file.read()
            files = {'file': ('dataset.csv', file_content, 'text/csv')}
            data = {
                'column_mapping': json.dumps(mapping)
            }
            if date_format:
                data['date_format'] = date_format
            
            try:
                response = requests.post(
                    f"{API_BASE_URL}/validate-columns",
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.dataset_info = result.get('dataset_info')
                    st.success("✅ Column mapping validated successfully!")
                    
                    # Show dataset info
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Records", result['dataset_info']['total_records'])
                    with col2:
                        st.metric("Total Amount", f"${result['dataset_info']['total_amount']:.2f}")
                    with col3:
                        st.metric("Avg Transaction", f"${result['dataset_info']['average_transaction']:.2f}")
                    with col4:
                        start = result['dataset_info']['date_range']['start'][:10]
                        end = result['dataset_info']['date_range']['end'][:10]
                        st.metric("Date Range", f"{start} to {end}")
                    
                    st.info("🚀 Ready! Go to **Dashboard** to view insights")
                else:
                    st.error(f"❌ Validation failed: {response.json().get('message')}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")

# ==================== DASHBOARD PAGE ====================
elif page == "Dashboard":
    st.header("📊 Business Insights Dashboard")
    
    if st.session_state.uploaded_file is None or not st.session_state.column_mapping:
        st.warning("⚠️ Please complete configuration first: Upload Dataset → Configure Columns")
        st.stop()
    
    # Analyze button
    if st.button("🔄 Generate Insights", width='stretch', type="primary", key="analyze_btn"):
        with st.spinner("🔄 Analyzing your data... This may take 1-2 minutes"):
            try:
                st.session_state.uploaded_file.seek(0)
                file_content = st.session_state.uploaded_file.read()
                files = {'file': ('dataset.csv', file_content, 'text/csv')}
                data = {
                    'column_mapping': json.dumps(st.session_state.column_mapping)
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/analyze-dynamic",
                    files=files,
                    data=data,
                    timeout=300
                )
                
                if response.status_code == 200:
                    results = response.json()
                    st.session_state.analysis_results = results
                    st.success("✅ Analysis complete!")
                else:
                    st.error(f"❌ Analysis failed: {response.json().get('message')}")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    
    # Display results if available
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        # ===== KPIs =====
        st.subheader("💼 Key Performance Indicators")
        if results.get('kpis'):
            kpis = results['kpis']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📈 Total Revenue", f"${kpis.get('total_revenue', 0):,.2f}")
            with col2:
                st.metric("📊 Avg Transaction", f"${kpis.get('average_order_value', 0):,.2f}")
            with col3:
                st.metric("✅ Success Rate", f"{kpis.get('success_rate', 0):.1f}%")
        
        # ===== Revenue Forecast =====
        st.subheader("📈 Revenue Forecast")
        if results.get('forecast'):
            forecast = results['forecast']
            
            col1, col2 = st.columns(2)
            with col1:
                forecast_values = forecast.get('next_months_forecast', [0])
                next_month = forecast_values[0] if forecast_values else 0
                st.metric("Next Month Forecast", f"${next_month:,.2f}")
            with col2:
                # Calculate confidence interval from forecast values
                if forecast_values:
                    confidence = f"{min(95, len(forecast_values) * 10):.0f}%"
                else:
                    confidence = "N/A"
                st.metric("Forecast Confidence", confidence)
            
            # Plot forecast (simplified visualization)
            try:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(12, 4))
                forecast_values = forecast.get('next_months_forecast', [])
                if forecast_values:
                    ax.plot(forecast_values, marker='o', linewidth=2, color='#1f77b4')
                    ax.set_title("Revenue Forecast")
                    ax.set_xlabel("Months")
                    ax.set_ylabel("Revenue ($)")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            except:
                st.info("Forecast data available: " + str(forecast))
        
        # ===== Risk Analysis =====
        st.subheader("⚠️ Risk Analysis & Anomalies")
        if results.get('risk_analysis'):
            risk = results['risk_analysis']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Anomalies Detected", risk.get('anomaly_count', 0))
            with col2:
                # Convert risk_level to a score
                risk_level_map = {"low": 20, "medium": 50, "high": 80}
                risk_score = risk_level_map.get(risk.get('risk_level', 'low'), 0)
                st.metric("Risk Score", f"{risk_score:.1f}/100")
            
            if risk.get('anomaly_days'):
                st.write("**Detected Anomalies:**")
                anomalies_df = pd.DataFrame({'Date': risk['anomaly_days'][:10]})
                st.dataframe(anomalies_df, width='stretch')
        
        # ===== Health Score =====
        st.subheader("🏥 Business Health Score")
        if results.get('health_score'):
            health = results['health_score']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                score = health.get('overall_score', 0)
                st.metric("Overall Health", f"{score:.1f}/100")
            with col2:
                st.metric("Revenue Health", f"{health.get('revenue_health', 0):.1f}%")
            with col3:
                st.metric("Stability", f"{health.get('stability_score', 0):.1f}%")
            
            status = health.get('status', 'Unknown')
            if status == 'Healthy':
                st.success(f"✅ Status: {status}")
            elif status == 'At Risk':
                st.warning(f"⚠️ Status: {status}")
            else:
                st.error(f"❌ Status: {status}")
        
        # ===== Recommendations =====
        st.subheader("💡 AI-Powered Recommendations")
        if results.get('recommendations'):
            recs = results['recommendations']
            # recs is a list, not a dict
            for i, rec in enumerate(recs[:5] if isinstance(recs, list) else [], 1):
                st.info(f"**{i}.** {rec}")
        
        # ===== AI Executive Summary =====
        st.subheader("🤖 AI Executive Summary")
        if results.get('ai_executive_summary'):
            st.write(results['ai_executive_summary'])
        
        # ===== Monte Carlo Analysis =====
        st.subheader("🎲 Monte Carlo Simulation Results")
        if results.get('monte_carlo'):
            mc = results['monte_carlo']
            col1, col2, col3 = st.columns(3)
            with col1:
                worst = mc.get('worst_case_revenue', 0)
                st.metric("Worst Case", f"${worst:,.2f}")
            with col2:
                best = mc.get('best_case_revenue', 0)
                st.metric("Best Case", f"${best:,.2f}")
            with col3:
                volatility = mc.get('volatility_index_percent', 0)
                st.metric("Volatility Index", f"{volatility:.2f}%")

# ==================== WHAT-IF ANALYSIS PAGE ====================
elif page == "What-If Analysis":
    st.header("🔮 What-If Scenario Analysis")
    
    if st.session_state.uploaded_file is None or not st.session_state.column_mapping:
        st.warning("⚠️ Please complete configuration first: Upload Dataset → Configure Columns")
        st.stop()
    
    st.markdown("""
    Test different scenarios and see how they would impact your business metrics.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_change = st.slider(
            "💰 Revenue Change (%)",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=1.0,
            help="Increase or decrease revenue by this percentage"
        )
    
    with col2:
        st.session_state.uploaded_file.seek(0)
        filter_col = st.selectbox(
            "🔍 Filter by Column (Optional)",
            options=[None] + list(pd.read_csv(st.session_state.uploaded_file).columns),
            help="Apply scenario to specific segment only"
        )
    
    if filter_col and filter_col != None:
        st.session_state.uploaded_file.seek(0)
        df = pd.read_csv(st.session_state.uploaded_file)
        available_values = df[filter_col].unique()[:20]  # Limit to first 20
        
        filter_value = st.selectbox(
            f"Select {filter_col}:",
            options=available_values
        )
    else:
        filter_value = None
    
    if st.button("▶️ Run What-If Scenario", width='stretch', type="primary"):
        with st.spinner("⏳ Running scenario analysis..."):
            try:
                st.session_state.uploaded_file.seek(0)
                file_content = st.session_state.uploaded_file.read()
                files = {'file': ('dataset.csv', file_content, 'text/csv')}
                data = {
                    'column_mapping': json.dumps(st.session_state.column_mapping),
                    'metric_change_percent': metric_change,
                }
                if filter_col and filter_value:
                    data['filter_column'] = filter_col
                    data['filter_value'] = str(filter_value)
                
                response = requests.post(
                    f"{API_BASE_URL}/what-if-dynamic",
                    files=files,
                    data=data,
                    timeout=300
                )
                
                if response.status_code == 200:
                    scenario = response.json()
                    st.success("✅ Scenario analysis complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Revenue Change", f"{metric_change:+.1f}%")
                    with col2:
                        st.metric("Affected Records", scenario['affected_records'])
                    with col3:
                        st.metric("New Forecast", f"${scenario['forecast'].get('next_month_forecast', 0):,.2f}")
                    
                    st.subheader("Scenario Impact")
                    st.json(scenario)
                else:
                    st.error(f"❌ Analysis failed: {response.json().get('message')}")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.markdown("**v2.0** | Built with Streamlit + FastAPI")
