import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Add Bootstrap to Streamlit for UI
st.markdown("""
<head>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
""", unsafe_allow_html=True)

# Add custom CSS
with open("app/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load preprocessed data
df = pd.read_csv(r'data/feature_engineered_incident_data.csv')

# Convert 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Convert to date (to avoid Timestamp issue with the slider)
df['date'] = df['timestamp'].dt.date

# Set the title of the dashboard
st.title("Incident Response Dashboard")

# Date filter slider
start_date = df['date'].min()
end_date = df['date'].max()

# Make sure the slider's min_value and max_value are datetime.date objects
selected_range = st.slider('Select Date Range', 
                           min_value=start_date, 
                           max_value=end_date, 
                           value=(start_date, end_date), 
                           format="YYYY-MM-DD")

# Filter the data based on selected date range
filtered_df = df[(df['date'] >= selected_range[0]) & (df['date'] <= selected_range[1])]

# Organize widgets in columns for better layout
col1, col2 = st.columns(2)

with col1:
    attack_type = st.selectbox("Select Attack Type", df['attack_type'].unique())

with col2:
    st.markdown("""<div class="container mt-4">
                    <h3 class="mt-4">Filter by Date</h3>
                    </div>""", unsafe_allow_html=True)

# Filtered Data based on selected attack type
filtered_attack_df = df[df['attack_type'] == attack_type]

# Attack Severity Trend over Time
fig1 = px.line(filtered_df, x='timestamp', y='severity', title="Attack Severity Over Time")
st.plotly_chart(fig1)

# Forecasted Attack Severity
fig2 = px.line(filtered_df, x='timestamp', y='severity_rolling_avg', title="Forecasted Attack Severity")
st.plotly_chart(fig2)

# Attack Severity for selected attack type
fig3 = px.line(filtered_attack_df, x='timestamp', y='severity', title=f"Attack Severity Over Time ({attack_type})")
st.plotly_chart(fig3)

# Forecasted Attack Severity for selected attack type
fig4 = px.line(filtered_attack_df, x='timestamp', y='severity_rolling_avg', title=f"Forecasted Attack Severity ({attack_type})")
st.plotly_chart(fig4)

# Additional Visualization: Distribution of Attack Types
fig5 = px.histogram(df, x='attack_type', title="Distribution of Attack Types")
st.plotly_chart(fig5)

# Additional Visualization: Distribution of Severity
fig6 = px.histogram(df, x='severity', title="Distribution of Attack Severity")
st.plotly_chart(fig6)

# Insights Section with Expander for clarity
with st.expander("See Insights"):
    st.markdown("""
    ### Insights:
    - The dashboard visualizes the attack severity trends over time, as well as the forecasted severity based on rolling averages.
    - Use the dropdown to filter by specific attack types and see their respective trends.
    - The histograms provide insights into the distribution of attack types and attack severities.
    - The dynamic charts update based on the selected date range and attack type.
    """)

# Additional Insights and Visualizations

# Top 5 Attacks by Severity
top_attacks = df.groupby('attack_type')['severity'].mean().sort_values(ascending=False).head(5)
st.write("Top 5 Attacks by Average Severity:")
st.bar_chart(top_attacks)

# Time of Day Trend: Attack Severity per Hour
df['hour'] = df['timestamp'].dt.hour
hour_trend = df.groupby('hour')['severity'].mean()
st.write("Attack Severity Trend by Hour of the Day:")
st.line_chart(hour_trend)

# Pie Chart for Attack Type Distribution
fig7 = px.pie(df, names='attack_type', title='Distribution of Attack Types')
st.plotly_chart(fig7)

# Custom Alert Feature based on Severity Threshold
severity_threshold = st.slider("Select Severity Threshold", min_value=1, max_value=10, value=5)
high_severity_df = df[df['severity'] > severity_threshold]
st.write(f"Incidents with severity higher than {severity_threshold}:")
st.write(high_severity_df)

# **Critical Severity Alert** - Notify the user when severity is higher than 8
if severity_threshold > 8:
    st.markdown("<h4 style='color:red;'>🚨 Critical Severity Alert! 🚨</h4>", unsafe_allow_html=True)

# Expanded Search Functionality (Allow search by attack description, attack type, or date)
search_query = st.text_input("Search for an attack type, description, or date:")
if search_query:
    search_columns = ['attack_type', 'attack_description', 'date']
    filtered_search_df = df[df[search_columns].apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.write(f"Search results for '{search_query}':")
    st.write(filtered_search_df)

# Optional: Show the number of results for user clarity
if search_query:
    result_count = filtered_search_df.shape[0]
    st.write(f"Total results found: {result_count}")
