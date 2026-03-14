#!/usr/bin/env python3
"""
Quick Start Script for Business Insights Generator
Run this to validate setup and start both frontend & backend
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_step(step_num, text):
    print(f"\n[Step {step_num}] {text}")
    print("-" * 50)

def check_python_version():
    """Check if Python version is 3.9+"""
    print_step(1, "Checking Python Version")
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)

def check_requirements():
    """Check if key packages are installed"""
    print_step(2, "Checking Required Packages")
    
    required = ['fastapi', 'streamlit', 'pandas', 'numpy', 'torch']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"✓ {pkg}")
        except ImportError:
            print(f"✗ {pkg} (missing)")
            missing.append(pkg)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        install = input("Install now? (y/n): ").lower() == 'y'
        if install:
            print("Installing packages...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirement.txt'])
            print("✓ Packages installed")

def check_data_folder():
    """Verify data files exist"""
    print_step(3, "Checking Data Files")
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    if (data_dir / "online_retail.csv").exists():
        print("✓ online_retail.csv found")
    else:
        print("⚠ online_retail.csv not found")
    
    if (data_dir / "superstore_sales.csv").exists():
        print("✓ superstore_sales.csv found")
    else:
        print("ℹ Generating superstore_sales.csv...")
        try:
            subprocess.run([sys.executable, 'generate_test_data.py'], check=True)
            print("✓ superstore_sales.csv generated")
        except:
            print("⚠ Could not generate test dataset")

def show_startup_options():
    """Show startup options"""
    print_header("STARTUP OPTIONS")
    
    print("\n1. Start Backend Only")
    print("   FastAPI server on http://localhost:8000")
    
    print("\n2. Start Frontend Only")
    print("   Streamlit app on http://localhost:8501")
    
    print("\n3. Start Both (Recommended)")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:8501")
    
    print("\n4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    return choice

def start_backend():
    """Start FastAPI backend"""
    print_step(4, "Starting Backend (FastAPI)")
    print("Command: uvicorn app.main:app --reload")
    print("Server: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("\nStarting in new terminal...\n")
    
    if sys.platform == 'win32':
        subprocess.Popen(['cmd.exe', '/c', 'start', 'cmd', '/k', 'uvicorn app.main:app --reload'])
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', '-a', 'Terminal', '--args', 'uvicorn app.main:app --reload'])
    else:  # Linux
        subprocess.Popen(['gnome-terminal', '--', 'uvicorn', 'app.main:app', '--reload'])

def start_frontend():
    """Start Streamlit frontend"""
    print_step(5, "Starting Frontend (Streamlit)")
    print("Command: streamlit run frontend/streamlit_app.py")
    print("App: http://localhost:8501")
    print("\nStarting...\n")
    
    subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'frontend/streamlit_app.py'])

def print_quick_guide():
    """Print quick usage guide"""
    print_header("QUICK START GUIDE")
    
    print("""
    🚀 Getting Started:
    
    1. UPLOAD DATASET
       - Go to "Upload Dataset" page
       - Choose CSV file or download test data
    
    2. MAP COLUMNS
       - Go to "Configure Columns" page
       - Select which columns contain:
         • Date (required)
         • Amount/Revenue (required)
         • Quantity (optional)
         • Country/Region (optional)
    
    3. VIEW INSIGHTS
       - Go to "Dashboard" page
       - Click "Generate Insights"
       - Wait 1-2 minutes for analysis
    
    4. RUN SCENARIOS
       - Go to "What-If Analysis"
       - Adjust revenue change %
       - Test different segments
    
    📊 Test Dataset:
    - Name: superstore_sales.csv
    - Records: 5,480 transactions
    - Columns: OrderDate, SalesAmount, Quantity, Region, Category
    - Date Range: 2022-2024
    
    📚 Documentation:
    - Backend: frontend/README.md
    - API Docs: http://localhost:8000/docs
    - Streamlit: http://localhost:8501
    """)

def main():
    # Check system
    print_header("BUSINESS INSIGHTS GENERATOR - STARTUP")
    print("Version: 2.0")
    print("Time:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    check_python_version()
    check_requirements()
    check_data_folder()
    
    choice = show_startup_options()
    
    if choice == '1':
        start_backend()
    elif choice == '2':
        start_frontend()
    elif choice == '3':
        print_step(4, "Starting Both Backend & Frontend")
        start_backend()
        time.sleep(3)
        start_frontend()
    elif choice == '4':
        print("\nExiting...")
        sys.exit(0)
    else:
        print("❌ Invalid option")
        sys.exit(1)
    
    print_quick_guide()
    
    print("\n✅ Startup Complete!")
    print("Open your browser if not already done.")
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
