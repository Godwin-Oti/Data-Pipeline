import streamlit as st
from psycopg2 import sql
from sqlalchemy import create_engine
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime
# Load environment variables
load_dotenv()

# Function to connect to the database
def get_connection():
    DATABASE_URL = st.secrets["DataBase_Url"]
    engine = create_engine(DATABASE_URL)
    return engine

# Function to fetch bitcoin prices from the database
def fetch_bitcoin_data(engine):
    query = "SELECT * FROM Bitcoin_Prices_Update ORDER BY date" 
    df = pd.read_sql_query(query, engine)
    return df

# Function to fetch bitcoin news from the database
def fetch_bitcoin_news(engine):
    query = "SELECT * FROM Bitcoin_News_Update" 
    df = pd.read_sql_query(query, engine)
    return df

# Get the database connection 
conn = get_connection()

# Fetch the bitcoin data and news
bitcoin_prices_df = fetch_bitcoin_data(conn)
bitcoin_news_df = fetch_bitcoin_news(conn)

# Display Bitcoin Prices 
st.title("Bitcoin Data")
st.line_chart(bitcoin_prices_df.set_index("date")["close"])

# Display Bitcoin News 
st.title("Bitcoin News")
st.write(bitcoin_news_df)

# Merge prices and news dataframes on the date column
merged_df = pd.merge(bitcoin_prices_df, bitcoin_news_df, on='date', how='left')

# Convert the date column to datetime format
merged_df['date'] = pd.to_datetime(merged_df['date'])

# Add a date range slider
date_range = st.slider("Select Date Range", merged_df['date'].min(), merged_df['date'].max(), (merged_df['date'].min(), merged_df['date'].max()))

# Filter the dataframe based on the selected date range
filtered_df = merged_df[(merged_df['date'] >= date_range[0]) & (merged_df['date'] <= date_range[1])]

# Create an interactive Plotly line chart
fig = px.line(filtered_df, x='date', y='close', title='Bitcoin Prices', labels={'close': 'BTC Price'})

# Add hover data for news headlines
fig.update_traces(mode='lines+markers', hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: %{y}<br><b>News</b>: %{customdata[0]}')
fig.update_traces(customdata=filtered_df[['title']].values)

# Display the Plotly chart
st.plotly_chart(fig)

# Display the Bitcoin news DataFrame
st.title("Bitcoin News")
st.write(bitcoin_news_df)
