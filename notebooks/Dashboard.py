import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Add Bootstrap for improved UI styling
st.markdown("""
<head>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
""", unsafe_allow_html=True)

# Load custom CSS
with open("app/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load and preprocess data
df = pd.read_csv(r'data/feature_engineered_incident_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour  # for time-of-day analysis

# Dashboard title
st.title("Incident Response Dashboard")

# Date range filter
start_date = df['date'].min()
end_date = df['date'].max()
selected_range = st.slider("Select Date Range", min_value=start_date, max_value=end_date, value=(start_date, end_date), format="YYYY-MM-DD")

# Filter by selected date range
filtered_df = df[(df['date'] >= selected_range[0]) & (df['date'] <= selected_range[1])]

# Layout: Filters
col1, col2 = st.columns(2)
with col1:
    attack_type = st.selectbox("Select Attack Type", df['attack_type'].unique())
with col2:
    st.markdown("""<div class="container mt-4"><h3 class="mt-4">Filter by Date</h3></div>""", unsafe_allow_html=True)

# Filter by selected attack type
filtered_attack_df = filtered_df[filtered_df['attack_type'] == attack_type]

# ---- Visualizations ----

# 1. Severity over time (full data)
st.plotly_chart(px.line(filtered_df, x='timestamp', y='severity', title="Attack Severity Over Time"))

# 2. Forecasted severity over time
st.plotly_chart(px.line(filtered_df, x='timestamp', y='severity_rolling_avg', title="Forecasted Attack Severity"))

# 3. Severity for selected attack type
st.plotly_chart(px.line(filtered_attack_df, x='timestamp', y='severity', title=f"Attack Severity Over Time ({attack_type})"))

# 4. Forecasted severity for selected attack type
st.plotly_chart(px.line(filtered_attack_df, x='timestamp', y='severity_rolling_avg', title=f"Forecasted Attack Severity ({attack_type})"))

# 5. Attack type distribution
st.plotly_chart(px.histogram(df, x='attack_type', title="Distribution of Attack Types"))

# 6. Severity distribution
st.plotly_chart(px.histogram(df, x='severity', title="Distribution of Attack Severity"))

# 7. Pie chart of attack types
st.plotly_chart(px.pie(df, names='attack_type', title='Distribution of Attack Types'))

# ---- Insights Section ----
with st.expander("🔍 See Insights"):
    st.markdown("""
    ### Insights:
    - The dashboard visualizes real-time and forecasted attack severity.
    - Filter by date range and attack type to explore trends.
    - Severity and frequency distributions highlight attack patterns.
    - Peak hours and top attack types are shown using time-based and categorical summaries.
    """)

# ---- Additional Visualizations ----

# 8. Top 5 attack types by average severity
top_attacks = df.groupby('attack_type')['severity'].mean().sort_values(ascending=False).head(5)
st.subheader("🔥 Top 5 Attacks by Average Severity")
st.bar_chart(top_attacks)

# 9. Severity trend by hour of day
hour_trend = df.groupby('hour')['severity'].mean()
st.subheader("🕒 Attack Severity Trend by Hour")
st.line_chart(hour_trend)

# ---- Severity Alerting and Filtering ----
severity_threshold = st.slider("Select Severity Threshold", min_value=1, max_value=10, value=5)
high_severity_df = df[df['severity'] > severity_threshold]

st.subheader(f"📈 Incidents with Severity > {severity_threshold}")
st.dataframe(high_severity_df)

if severity_threshold > 8:
    st.markdown("<h4 style='color:red;'>🚨 Critical Severity Alert! 🚨</h4>", unsafe_allow_html=True)

# ---- Search Functionality ----
search_query = st.text_input("🔎 Search by attack type, description, or date:")
if search_query:
    search_columns = ['attack_type', 'attack_description', 'date']
    filtered_search_df = df[df[search_columns].apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.subheader(f"🔍 Search Results for: `{search_query}`")
    st.dataframe(filtered_search_df)
    st.write(f"🔢 Total results found: {filtered_search_df.shape[0]}")
