# components/dashboard.py

import pandas as pd
import plotly.express as px
import streamlit as st

def create_dashboard(projects):
    # Convert SQLAlchemy objects to plain dicts, excluding SQLAlchemy metadata
    data = []
    for p in projects:
        if hasattr(p, "__dict__"):
            project_data = {k: v for k, v in p.__dict__.items() if not k.startswith("_")}
        else:
            project_data = p
        data.append(project_data)

    df = pd.DataFrame(data)

    if df.empty:
        st.warning("No project data available for dashboard.")
        return

    # Main Dashboard: Risk Score Bar Chart
    st.subheader("📊 Overview of Project Risk Scores")
    fig = px.bar(
        df,
        x="name",
        y="risk_score",
        color="risk_score",
        color_continuous_scale="RdYlGn_r",
        labels={"risk_score": "Risk Score", "name": "Project"},
        title="Overall Risk Score by Project"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Schedule Risk Line Chart
    st.subheader("🕒 Schedule Risk")
    fig = px.line(
        df,
        x="name",
        y="schedule_risk",
        markers=True,
        title="Schedule Risk Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Budget Risk Bar Chart
    st.subheader("💸 Budget Risk")
    fig = px.bar(
        df,
        x="name",
        y="budget_risk",
        color="budget_risk",
        color_continuous_scale="OrRd",
        title="Budget Risk Levels"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Market Risk Bubble Plot
    st.subheader("📉 Market Risk Trend")
    fig = px.scatter(
        df,
        x="name",
        y="market_risk",
        size="market_risk",
        color="market_risk",
        color_continuous_scale="Bluered",
        title="Market Risk Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
