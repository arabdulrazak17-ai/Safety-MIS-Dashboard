import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Safety MIS Dashboard",
    page_icon="🦺",
    layout="wide"
)

# Load data
df = pd.read_csv("analysis_data.csv")

# Title
st.title("🦺 Safety Observations MIS Dashboard")

st.markdown(
    """
    **Management Information System (MIS)**
    
    Safety observations analysis for August 2026 across multiple locations.
    """
)

st.info(
    "📌 Note: Week 31 and Week 36 are partial weeks because the source data "
    "covers August 2026 only."
)


# -------------------------
# Dashboard Filters
# -------------------------

st.subheader("Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    selected_category = st.multiselect(
        "Category",
        options=sorted(df["Category"].dropna().unique()),
        default=sorted(df["Category"].dropna().unique())
    )

with filter_col2:
    selected_risk = st.multiselect(
        "Risk Level",
        options=sorted(df["Risk Level Clean"].dropna().unique()),
        default=sorted(df["Risk Level Clean"].dropna().unique())
    )

with filter_col3:
    selected_action = st.multiselect(
        "Action Status",
        options=sorted(df["Action Status"].dropna().unique()),
        default=sorted(df["Action Status"].dropna().unique())
    )
with filter_col4:

    week_options = sorted(df["Week"].dropna().unique())

    selected_week_labels = st.multiselect(
        "Week",
        options=[f"Week {int(w)}" for w in week_options],
        default=[f"Week {int(w)}" for w in week_options]
    )

    selected_weeks = [
        int(w.replace("Week ", ""))
        for w in selected_week_labels
    ]   
# Apply selected filters

filtered_df = df[
    df["Category"].isin(selected_category)
    & df["Risk Level Clean"].isin(selected_risk)
    & df["Action Status"].isin(selected_action)
    & df["Week"].isin(selected_weeks)
].copy()

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} observations"
)

# KPI calculations using filtered data
total_observations = len(filtered_df)

actions_assigned = filtered_df["Action Assigned"].sum()

overdue_actions = (
    filtered_df["Action Status"] == "Overdue"
).sum()

# Count observations belonging to repeated Location + Type patterns
pattern_counts = (
    filtered_df.groupby(["Location", "Type"])["Observation Id"]
    .transform("count")
)

repeated_observations = (pattern_counts > 1).sum()

# Calculate percentages safely
action_assignment_rate = (
    actions_assigned / total_observations * 100
    if total_observations > 0 else 0
)

overdue_rate = (
    overdue_actions / actions_assigned * 100
    if actions_assigned > 0 else 0
)

repeated_rate = (
    repeated_observations / total_observations * 100
    if total_observations > 0 else 0
)
    
# -------------------------
# KPI Cards
# -------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Observations",
        f"{total_observations:,}"
    )
    st.caption("Total safety observations")

with col2:
    st.metric(
        "Actions Assigned",
        f"{actions_assigned:,}"
    )
    st.caption(
        f"{action_assignment_rate:.1f}% of observations"
    )

with col3:
    st.metric(
        "Overdue Actions",
        f"{overdue_actions:,}"
    )
    st.caption(
        f"{overdue_rate:.1f}% of assigned actions"
    )

with col4:
    st.metric(
        "Repeated Observations",
        f"{repeated_observations:,}"
    )
    st.caption(
        f"{repeated_rate:.1f}% of observations"
    )
    
st.markdown("---")
st.subheader("📈 Trend & Forecast")    
# -------------------------
# Weekly Trend + WoW Analysis
# -------------------------

col1, col2 = st.columns(2)

# Weekly Observation Trend
with col1:

    weekly = (
        filtered_df.groupby("Week")
        .size()
        .reset_index(name="Observations")
        .sort_values("Week")
    )

    weekly["Week"] = "Week " + weekly["Week"].astype(str)

    fig_weekly = px.line(
        weekly,
        x="Week",
        y="Observations",
        markers=True,
        title="Weekly Observation Trend"
    )

    fig_weekly.update_layout(
        xaxis_title="Week",
        yaxis_title="Observations",
        height=420
    )

    st.plotly_chart(
        fig_weekly,
        use_container_width=True,
        key="weekly_chart"
    )


# Week-on-Week Change
with col2:

    st.subheader("Week-on-Week Change")

    wow = (
        filtered_df.groupby("Week")
        .size()
        .reset_index(name="Observations")
        .sort_values("Week")
    )

    wow["WoW Change %"] = (
        wow["Observations"]
        .pct_change()
        .mul(100)
    )

    wow["Week"] = "Week " + wow["Week"].astype(str)

    st.dataframe(
        wow,
        use_container_width=True,
        hide_index=True,
        column_config={
            "WoW Change %": st.column_config.NumberColumn(
                "WoW Change %",
                format="%.1f%%"
            )
        }
    )

# -------------------------
# Predictive Trend
# -------------------------

st.subheader("Predictive Trend")

st.caption(
    "Estimated forecast based on a simple linear trend using the "
    "more complete weeks (Weeks 32–35)."
)

forecast_data = (
    filtered_df.groupby("Week")
    .size()
    .reset_index(name="Observations")
    .sort_values("Week")
)

# Use Weeks 32–35 because Week 31 and Week 36 are partial weeks
forecast_history = forecast_data[
    forecast_data["Week"].isin([32, 33, 34, 35])
].copy()

if len(forecast_history) >= 2:

    x = forecast_history["Week"].to_numpy()
    y = forecast_history["Observations"].to_numpy()

    # Fit a simple linear trend
    slope, intercept = np.polyfit(x, y, 1)

    future_weeks = np.array([37, 38, 39])

    forecast_values = (
        slope * future_weeks + intercept
    )

    forecast_values = np.maximum(
        0,
        np.round(forecast_values)
    ).astype(int)

    forecast_df = pd.DataFrame({
        "Week": ["Week 37", "Week 38", "Week 39"],
        "Estimated Observations": forecast_values
    })

    # Forecast chart
    fig_forecast = px.line(
        forecast_df,
        x="Week",
        y="Estimated Observations",
        markers=True,
        text="Estimated Observations",
        title="Forecast for Next 3 Weeks"
    )

    fig_forecast.update_traces(
        textposition="top center"
    )

    fig_forecast.update_layout(
        xaxis_title="Week",
        yaxis_title="Estimated Observations",
        height=400
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True,
        key="forecast_chart"
    )

    # Forecast table
    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "Not enough weekly data available to calculate a forecast."
    )
    
st.markdown("---")
st.subheader("💡 Key Insights")
    
# -------------------------
# Key Insights
# -------------------------

st.subheader("Key Insights")

# Calculate the main category
category_counts = filtered_df["Category"].value_counts()

if len(category_counts) > 0:
    top_category = category_counts.index[0]
    top_category_count = category_counts.iloc[0]
    top_category_pct = (
        top_category_count / len(filtered_df) * 100
    )
else:
    top_category = "N/A"
    top_category_count = 0
    top_category_pct = 0

# Highest observation location
location_counts = filtered_df["Location"].value_counts()

if len(location_counts) > 0:
    top_location = location_counts.index[0]
    top_location_count = location_counts.iloc[0]
else:
    top_location = "N/A"
    top_location_count = 0

# Highest observation week
week_counts = filtered_df["Week"].value_counts()

if len(week_counts) > 0:
    peak_week = week_counts.idxmax()
    peak_week_count = week_counts.max()
else:
    peak_week = "N/A"
    peak_week_count = 0

# Create insight columns
insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.info(
        f"**Category Insight**\n\n"
        f"{top_category} is the most frequently observed category, "
        f"with {top_category_count:,} observations "
        f"({top_category_pct:.1f}% of the filtered data)."
    )

    st.info(
        f"**Location Insight**\n\n"
        f"{top_location} has the highest number of observations, "
        f"with {top_location_count:,} observations."
    )

with insight_col2:

    st.info(
        f"**Weekly Insight**\n\n"
        f"Week {peak_week} recorded the highest number of observations "
        f"with {peak_week_count:,} observations."
    )

    st.info(
        f"**Action Insight**\n\n"
        f"{overdue_actions:,} observations currently have overdue actions, "
        f"representing {overdue_rate:.1f}% of observations with assigned actions."
    )
    
st.markdown("---")
st.subheader("📊 Observation Analysis")        

# -------------------------
# Category Analysis
# -------------------------

st.subheader("Category Analysis")

category = (
    filtered_df["Category"]
    .value_counts()
    .reset_index()
)

category.columns = ["Category", "Observations"]

fig_category = px.bar(
    category,
    x="Category",
    y="Observations",
    title="Observations by Category"
)

fig_category.update_layout(
    xaxis_title="Category",
    yaxis_title="Observations",
    height=420
)

st.plotly_chart(
    fig_category,
    use_container_width=True,
    key="category_chart"
)
    
 # -------------------------
# Charts row 2
# -------------------------

col1, col2 = st.columns(2)


# -------------------------
# Action Status
# -------------------------

with col1:

    action_status = (
        filtered_df["Action Status"]
        .value_counts()
        .reset_index()
    )

    action_status.columns = ["Action Status", "Observations"]

    fig_action = px.bar(
        action_status,
        x="Action Status",
        y="Observations",
        title="Action Status"
    )

    fig_action.update_layout(
        xaxis_title="Action Status",
        yaxis_title="Observations",
        height=420
    )

    st.plotly_chart(
        fig_action,
        use_container_width=True,
        key="action_chart"
    )


# -------------------------
# Risk Level
# -------------------------

with col2:

    risk = (
        filtered_df["Risk Level Clean"]
        .value_counts()
        .reset_index()
    )

    risk.columns = ["Risk Level", "Observations"]

    fig_risk = px.bar(
        risk,
        x="Risk Level",
        y="Observations",
        title="Observations by Risk Level"
    )

    fig_risk.update_layout(
        xaxis_title="Risk Level",
        yaxis_title="Observations",
        height=420
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        key="risk_chart"
    )
    
    # -------------------------
# Top 10 Locations
# -------------------------

st.subheader("Top 10 Locations by Observations")

location = (
    filtered_df["Location"]
    .value_counts()
    .head(10)
    .reset_index()
)

location.columns = ["Location", "Observations"]

fig_location = px.bar(
    location,
    x="Observations",
    y="Location",
    orientation="h",
    title="Top 10 Locations",
    text="Observations"
)

fig_location.update_yaxes(
    categoryorder="total ascending"
)

fig_location.update_layout(
    xaxis_title="Observations",
    yaxis_title="Location",
    height=500
)

st.plotly_chart(
    fig_location,
    use_container_width=True
)

st.markdown("---")
st.subheader("⚙️ Action Management")

# -------------------------
# Action Management
# -------------------------

st.subheader("Action Management")

action_summary = (
    filtered_df["Action Status"]
    .value_counts()
    .reindex(
        ["Completed", "Closed", "Open", "Overdue", "No Action"],
        fill_value=0
    )
    .reset_index()
)

action_summary.columns = ["Action Status", "Count"]

# Calculate percentage
action_summary["Percentage"] = (
    action_summary["Count"]
    / len(filtered_df)
    * 100
)

st.dataframe(
    action_summary,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Percentage": st.column_config.NumberColumn(
            "Percentage",
            format="%.1f%%"
        )
    }
)

# -------------------------
# Overdue Actions by Location
# -------------------------

st.subheader("Overdue Actions by Location")

st.caption(
    "Top locations ranked by the number of observations with overdue actions."
)

overdue_location = (
    filtered_df.loc[
        filtered_df["Action Status"] == "Overdue",
        "Location"
    ]
    .value_counts()
    .head(10)
    .reset_index()
)

overdue_location.columns = ["Location", "Overdue Actions"]

fig_overdue = px.bar(
    overdue_location,
    x="Overdue Actions",
    y="Location",
    orientation="h",
    title="Top 10 Locations by Overdue Actions",
    text="Overdue Actions"
)

fig_overdue.update_yaxes(
    categoryorder="total ascending"
)

fig_overdue.update_layout(
    xaxis_title="Overdue Actions",
    yaxis_title="Location",
    height=500
)

st.plotly_chart(
    fig_overdue,
    use_container_width=True,
    key="overdue_location_chart"
)

st.markdown("---")
st.subheader("🔁 Repeated Observations")

# -------------------------
# Repeated Observations
# -------------------------

st.subheader("Repeated Observations")

st.caption(
    "Repeated observations are identified when the same Location + Type "
    "combination occurs more than once."
)

repeated_count = (
    filtered_df["Repeated Observation"]
    .sum()
)

repeated_percentage = (
    repeated_count / len(filtered_df) * 100
    if len(filtered_df) > 0 else 0
)

st.metric(
    "Repeated Observations",
    f"{repeated_count:,}",
    f"{repeated_percentage:.1f}% of observations"
)

repeated_patterns = (
    filtered_df
    .groupby(["Location", "Type"])
    .size()
    .reset_index(name="Count")
)

repeated_patterns = (
    repeated_patterns[repeated_patterns["Count"] > 1]
    .sort_values("Count", ascending=False)
    .head(10)
)

repeated_patterns["Pattern"] = (
    repeated_patterns["Location"] + " — " +
    repeated_patterns["Type"]
)

fig_repeated = px.bar(
    repeated_patterns,
    x="Count",
    y="Pattern",
    orientation="h",
    title="Top 10 Repeated Observation Patterns",
    text="Count"
)

fig_repeated.update_yaxes(
    categoryorder="total ascending"
)

fig_repeated.update_layout(
    xaxis_title="Number of Occurrences",
    yaxis_title="Location + Type",
    height=550
)

st.plotly_chart(
    fig_repeated,
    use_container_width=True,
    key="repeated_observations_chart"
)

st.markdown("---")
st.subheader("⚠️ Severity Analysis")

# -------------------------
# Risk / Severity Analysis
# -------------------------

st.subheader("Risk / Severity Analysis")

st.caption(
    "High-severity observations are defined as Serious or Fatal risk levels. "
    "The charts show the Top 5 and Bottom 5 locations based on high-severity observations."
)

severity_col1, severity_col2 = st.columns(2)

with severity_col1:

    high_risk_count = len(
        filtered_df[
            filtered_df["Risk Level Clean"].isin(["Serious", "Fatal"])
        ]
    )

    st.metric(
        "Serious + Fatal Observations",
        f"{high_risk_count:,}"
    )

with severity_col2:

    fatal_count = (
        filtered_df["Risk Level Clean"] == "Fatal"
    ).sum()

    st.metric(
        "Fatal Observations",
        f"{fatal_count:,}"
    )

high_risk = filtered_df[
    filtered_df["Risk Level Clean"].isin(["Serious", "Fatal"])
]

severity_location = (
    high_risk["Location"]
    .value_counts()
    .head(5)
    .reset_index()
)

severity_location.columns = [
    "Location",
    "Serious + Fatal Observations"
]

fig_severity_top = px.bar(
    severity_location,
    x="Serious + Fatal Observations",
    y="Location",
    orientation="h",
    title="Top 5 Locations by Serious + Fatal Observations",
    text="Serious + Fatal Observations"
)

fig_severity_top.update_yaxes(
    categoryorder="total ascending"
)

fig_severity_top.update_layout(
    xaxis_title="Serious + Fatal Observations",
    yaxis_title="Location",
    height=450
)

st.plotly_chart(
    fig_severity_top,
    use_container_width=True,
    key="severity_top5_chart"
)

# -------------------------
# Bottom 5 High-Severity Locations
# -------------------------

severity_location_all = (
    high_risk["Location"]
    .value_counts()
    .reset_index()
)

severity_location_all.columns = [
    "Location",
    "Serious + Fatal Observations"
]

bottom_5 = (
    severity_location_all
    .sort_values("Serious + Fatal Observations", ascending=True)
    .head(5)
)

fig_severity_bottom = px.bar(
    bottom_5,
    x="Serious + Fatal Observations",
    y="Location",
    orientation="h",
    title="Bottom 5 Locations with Serious + Fatal Observations",
    text="Serious + Fatal Observations"
)

fig_severity_bottom.update_yaxes(
    categoryorder="total descending"
)

fig_severity_bottom.update_layout(
    xaxis_title="Serious + Fatal Observations",
    yaxis_title="Location",
    height=450
)

st.plotly_chart(
    fig_severity_bottom,
    use_container_width=True,
    key="severity_bottom5_chart"
)