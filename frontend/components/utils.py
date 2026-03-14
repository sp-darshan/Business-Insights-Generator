import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_forecast_chart(forecast_data, title="Revenue Forecast"):
    """Create a forecast visualization"""
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if isinstance(forecast_data, dict):
        values = forecast_data.get('forecast_values', [])
    else:
        values = forecast_data
    
    if values:
        ax.plot(values, marker='o', linewidth=2.5, color='#1f77b4', markersize=6)
        ax.fill_between(range(len(values)), values, alpha=0.2, color='#1f77b4')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel("Time Period", fontsize=11)
        ax.set_ylabel("Revenue ($)", fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
    
    return fig


def plot_anomalies_heatmap(anomalies_data, title="Anomaly Detection Heatmap"):
    """Create anomaly detection visualization"""
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if isinstance(anomalies_data, list) and len(anomalies_data) > 0:
        df_anomalies = pd.DataFrame(anomalies_data[:30])
        if 'score' in df_anomalies.columns:
            colors = ['#dc3545' if x > 0.7 else '#ffc107' for x in df_anomalies['score']]
            ax.bar(range(len(df_anomalies)), df_anomalies['score'], color=colors)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xlabel("Anomaly Index", fontsize=11)
            ax.set_ylabel("Anomaly Score", fontsize=11)
            ax.axhline(y=0.7, color='r', linestyle='--', alpha=0.5, label='Critical Threshold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
    
    return fig


def plot_health_gauge(score, title="Health Score"):
    """Create a gauge chart for health score"""
    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(projection='polar'))
    
    # Normalize score to 0-2π
    theta = np.linspace(0, np.pi, 100)
    r = np.ones(100)
    
    color = '#28a745' if score >= 70 else '#ffc107' if score >= 50 else '#dc3545'
    
    ax.barh(theta, r, width=0.5, alpha=0.3, color='lightgray')
    ax.barh(theta[:int(len(theta)*score/100)], r[:int(len(r)*score/100)], width=0.5, color=color)
    
    ax.set_ylim(0, 1)
    ax.set_theta_offset(np.pi)
    ax.set_theta_direction(-1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add score text
    ax.text(0, 0, f'{score:.0f}', ha='center', va='center', fontsize=20, fontweight='bold')
    
    return fig


def display_metric_card(label, value, icon="📊", delta=None):
    """Display a styled metric card"""
    col = st.columns(1)[0]
    with col:
        if delta:
            st.metric(f"{icon} {label}", value, delta=delta)
        else:
            st.metric(f"{icon} {label}", value)


def display_recommendations(recommendations, max_items=5):
    """Display recommendations in a nice format"""
    st.subheader("💡 Top Recommendations")
    
    if isinstance(recommendations, dict):
        recs_list = recommendations.get('recommendations', [])
    else:
        recs_list = recommendations
    
    for i, rec in enumerate(recs_list[:max_items], 1):
        with st.container():
            col1, col2 = st.columns([0.5, 9.5])
            with col1:
                st.write(f"**{i}.**")
            with col2:
                st.write(rec)
            st.divider()


def format_currency(value):
    """Format value as currency"""
    if isinstance(value, (int, float)):
        return f"${value:,.2f}"
    return str(value)


def format_percentage(value):
    """Format value as percentage"""
    if isinstance(value, (int, float)):
        return f"{value:.1f}%"
    return str(value)
