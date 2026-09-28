# 🦺 Safety Observations MIS Dashboard

An interactive Management Information System (MIS) dashboard built using Python, Pandas, Plotly, and Streamlit to analyze safety observations across multiple locations.

## 📌 Project Overview

This project was developed as an interactive dashboard for analyzing safety observations recorded during August 2026.

The dashboard helps users understand:

- Weekly observation trends
- Week-on-week percentage changes
- Observation categories and types
- Observation distribution by location
- Action assignment and action status
- Overdue actions by location
- Repeated observation patterns
- Risk and severity levels
- Estimated trends for the next 3 weeks

## 🎯 Objectives

The main objectives of the dashboard are to:

1. Monitor weekly safety observation trends.
2. Analyze observations by category and risk level.
3. Identify locations with high observation volumes.
4. Track assigned, completed, open, closed, and overdue actions.
5. Identify repeated observation patterns.
6. Highlight locations with Serious and Fatal observations.
7. Provide an estimated forecast for the next 2–3 weeks.

## 📊 Key Dashboard Features

### 1. Interactive Filters

Users can filter the dashboard by:

- Category
- Risk Level
- Action Status
- Week

All dashboard metrics and visualizations update based on the selected filters.

### 2. KPI Summary

The dashboard provides key performance indicators including:

- Total Observations
- Actions Assigned
- Overdue Actions
- Repeated Observations

### 3. Weekly Trend Analysis

A weekly line chart shows the number of observations recorded during each week.

The dashboard also calculates the percentage change from one week to the next.

> Note: Week 31 and Week 36 are partial weeks because the source data covers August 2026 only.

### 4. Predictive Trend

A simple linear trend is used to estimate observations for the next three weeks.

Current estimated values:

| Week | Estimated Observations |
|------|------------------------:|
| Week 37 | 810 |
| Week 38 | 914 |
| Week 39 | 1,019 |

These values are estimates based on the more complete weeks (Weeks 32–35) and should not be interpreted as guaranteed future values.

### 5. Category Analysis

Observations are analyzed by category, including:

- Unsafe Condition
- Unsafe Act
- Best Practices
- QA - Observations
- LSR Violation

### 6. Action Management

The dashboard tracks action status:

- Completed
- Closed
- Open
- Overdue
- No Action

It also displays the percentage distribution of each status.

### 7. Overdue Actions by Location

The dashboard identifies locations with the highest number of overdue actions.

### 8. Repeated Observations

Repeated observations are identified when the same:

**Location + Type**

combination occurs more than once.

The dashboard displays:

- Total repeated observations
- Repeated observation percentage
- Top repeated observation patterns

### 9. Risk / Severity Analysis

High-severity observations are defined as:

- Serious
- Fatal

The dashboard provides:

- Top 5 locations by Serious + Fatal observations
- Bottom 5 locations with Serious + Fatal observations
- Total Serious + Fatal observations
- Total Fatal observations

## 📈 Key Results

Based on the available dataset:

- **Total Observations:** 1,974
- **Actions Assigned:** 537
- **Action Assignment Rate:** 27.2%
- **Overdue Actions:** 269
- **Overdue Rate among Assigned Actions:** 50.1%
- **Repeated Observations:** 938
- **Repeated Observation Rate:** 47.5%
- **Serious + Fatal Observations:** 181
- **Fatal Observations:** 3

## 🛠️ Technology Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- OpenPyXL

## 📂 Project Structure

```text
Mis_dashboard/
│
├── data/
│   └── Observations.xlsx
│
├── dashboard.py
├── analysis_data.csv
├── requirements.txt
├── README.md
└── .gitignore