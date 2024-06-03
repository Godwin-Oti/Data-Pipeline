import streamlit as st
import psycopg2
from sqlalchemy import create_engine
import os
import pandas as pd
import requests
from dotenv import load_dotenv


# DataBase connection parameters
load_dotenv()

# 
# Function to connect to the Database
def get_connection():
    # Use st.secrets to get the DATABASE_URL
    DATABASE_URL = st.secrets["DataBase_Url"]["url"]
    # Create an engine instance
    engine = create_engine(DATABASE_URL)
    return engine

# Function to fetch bitcoin prices from Database
def fetch_bitcoin_data(engine):
    # Query to fetch data
    query = "SELECT * FROM Bitcoin_Prices_Update ORDER BY date" 

    df = pd.read_sql_query(query, engine)
    
    return df
# Function to fetch bitcoin news from Database
def fetch_bitcoin_news(engine):
    # Query to fetch data
    query = "SELECT * FROM Bitcoin_News_Update" 

    df = pd.read_sql_query(query, engine)
    
    return df

# Get the database connection 
conn= get_connection()
# fetch the bitcoin data and news
bitcoin_prices_df=fetch_bitcoin_data(conn)
bitcoin_news_df=fetch_bitcoin_news(conn)

# Display Bitcoin Prices 
st.title("Bitcoin Data")
st.line_chart(bitcoin_prices_df.set_index("date")["close"])

# Display Bitcoin News 
st.title("Bitcoin News")
st.write(bitcoin_news_df)




