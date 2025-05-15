import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="UK Train Rides Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("railway.csv")
    return df

df = load_data()

# Preprocess data
def preprocess_data(df):
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'], format='%H:%M:%S', errors='coerce')
    df['Actual Arrival Time'] = pd.to_datetime(df['Actual Arrival Time'], format='%H:%M:%S', errors='coerce')
    df['Delayed Minutes'] = (df['Actual Arrival Time'] - df['Arrival Time']).dt.total_seconds() / 60
    df['Delayed Minutes'] = df['Delayed Minutes'].fillna(0).astype(int)
    df['Refund Requested'] = df['Refund Request'].apply(lambda x: 1 if x == 'Yes' else 0)
    df['Railcard'] = df['Railcard'].replace('None', 'No Railcard').fillna('No Railcard')
    df['Departure Time'] = pd.to_datetime(df['Departure Time'], format='%H:%M:%S', errors='coerce')
    df['Actual trip time'] = (df['Arrival Time'] - df['Departure Time']).dt.total_seconds() / 60
    df['Price Category'] = pd.cut(df['Price'], bins=[0, 5, 10, 20], labels=['Low', 'Medium', 'High'])
    return df

df = preprocess_data(df)

# Sidebar filters with expanders
st.sidebar.header("⚙️ Data Filters")

with st.sidebar.expander("Select Railcard Type", expanded=True):
    railcard_filter = st.multiselect("Railcard Type", options=df['Railcard'].unique(), default=df['Railcard'].unique())

with st.sidebar.expander("Select Ticket Class", expanded=True):
    ticket_class_filter = st.multiselect("Ticket Class", options=df['Ticket Class'].unique(), default=df['Ticket Class'].unique())

with st.sidebar.expander("Select Purchase Type", expanded=True):
    purchase_type_filter = st.multiselect("Purchase Type", options=df['Purchase Type'].unique(), default=df['Purchase Type'].unique())

# Apply filters
filtered_df = df[
    (df['Railcard'].isin(railcard_filter)) &
    (df['Ticket Class'].isin(ticket_class_filter)) &
    (df['Purchase Type'].isin(purchase_type_filter))
]

# Title
st.title("📊  UK Train Rides Dashboard")

# Overall metrics
st.markdown("### 📈 Overall Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Delay (minutes)", f"{filtered_df['Delayed Minutes'].mean():.2f}")
col2.metric("Refund Request Rate", f"{filtered_df['Refund Requested'].mean()*100:.2f}%")
col3.metric("Avg. Ticket Price (£)", f"{filtered_df['Price'].mean():.2f}")

# Railcard analysis
st.markdown("### 🎟️ Refund Rate by Railcard Type")
railcard_analysis = filtered_df.groupby('Railcard').agg({
    'Delayed Minutes': 'mean',
    'Refund Requested': 'mean'
}).reset_index()
fig1 = px.bar(railcard_analysis, x='Railcard', y='Refund Requested', title='Refund Rate by Railcard')
st.plotly_chart(fig1, use_container_width=True)

# Ticket class analysis
st.markdown("### 🪑 Refund Rate by Ticket Class")
class_analysis = filtered_df.groupby('Ticket Class').agg({
    'Delayed Minutes': 'mean',
    'Refund Requested': 'mean'
}).reset_index()
fig2 = px.bar(class_analysis, x='Ticket Class', y='Refund Requested', title='Refund Rate by Ticket Class')
st.plotly_chart(fig2, use_container_width=True)

# Purchase type analysis
st.markdown("### 🛒 Refund Rate by Purchase Type")
purchase_analysis = filtered_df.groupby('Purchase Type').agg({
    'Delayed Minutes': 'mean',
    'Refund Requested': 'mean'
}).reset_index()
fig3 = px.bar(purchase_analysis, x='Purchase Type', y='Refund Requested', title='Refund Rate by Purchase Type')
st.plotly_chart(fig3, use_container_width=True)

# Price vs delay
st.markdown("### 💷 Price vs Delay")
fig4 = px.scatter(filtered_df, x='Price', y='Delayed Minutes', color='Refund Requested', title='Ticket Price vs Delay')
st.plotly_chart(fig4, use_container_width=True)

# Refund by price category
st.markdown("### 📊 Refund Rate by Price Category")
price_category_analysis = filtered_df.groupby('Price Category').agg({
    'Delayed Minutes': 'mean',
    'Refund Requested': 'mean'
}).reset_index()
fig5 = px.bar(price_category_analysis, x='Price Category', y='Refund Requested', title='Refund Rate by Price Category')
st.plotly_chart(fig5, use_container_width=True)

# Delay reasons
st.markdown("### 🕒 Top Delay Reasons")
delay_reasons = filtered_df[filtered_df['Delayed Minutes'] > 0]['Reason for Delay'].value_counts().head(10)
fig6 = px.bar(delay_reasons, x=delay_reasons.index, y=delay_reasons.values, title='Top 10 Delay Reasons')
st.plotly_chart(fig6, use_container_width=True)



