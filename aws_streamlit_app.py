import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to connect to the Database
def get_connection():
    DATABASE_URL = st.secrets["DataBase_Url"]
    engine = create_engine(DATABASE_URL)
    return engine

# Function to fetch bitcoin prices from Database
def fetch_bitcoin_data(engine):
    query = "SELECT * FROM bitcoin_prices_aws ORDER BY date"
    df = pd.read_sql_query(query, engine)
    return df

# Function to fetch bitcoin news from Database
def fetch_bitcoin_news(engine):
    query = "SELECT * FROM bitcoin_news_aws ORDER BY date"
    df = pd.read_sql_query(query, engine)
    return df

# Get the database connection
conn = get_connection()

# Fetch the bitcoin data and news
bitcoin_prices_df = fetch_bitcoin_data(conn)
bitcoin_news_df = fetch_bitcoin_news(conn)

# Merge prices and news dataframes on the date column
merged_df = pd.merge(bitcoin_prices_df, bitcoin_news_df, on='date', how='left')

# Convert the date column to datetime format
merged_df['date'] = pd.to_datetime(merged_df['date'])

# Convert pandas Timestamps to datetime.date
min_date = merged_df['date'].min().date()
max_date = merged_df['date'].max().date()

# Sidebar for date selection
st.sidebar.title("Controls")
date_range = st.sidebar.slider("Select Date Range", min_date, max_date, (min_date, max_date))

# Filter the dataframe based on the selected date range
filtered_df = merged_df[(merged_df['date'] >= pd.to_datetime(date_range[0])) & (merged_df['date'] <= pd.to_datetime(date_range[1]))]

# Main Dashboard
st.title("Bitcoin Dashboard (Automated Data Pipeline)")

# Tabs for organizing content
tab1, tab2, tab3 = st.tabs(["Price Chart", "Candlestick Chart", "Additional Analysis"])

with tab1:
    # Creating a Plotly line chart with tooltips for news
    st.subheader("Bitcoin Prices")
    fig = px.line(filtered_df, x='date', y='close', title='Bitcoin Prices', labels={'close': 'BTC Price'})
    fig.update_traces(mode='lines+markers', hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: %{y}<br><b>News</b>: %{customdata[0]}')
    fig.update_traces(customdata=filtered_df[['title']].values)
    st.plotly_chart(fig)
    
    # Displaying the dataframe with bitcoin news
    st.subheader("Bitcoin News")
    
    st.dataframe(filtered_df[['date', 'title']], width=1000) # Increased width to 1000 pixels 

with tab2:
    # Candlestick Chart
    st.subheader("Bitcoin Candlestick Chart")
    fig_candlestick = go.Figure(data=[go.Candlestick(x=filtered_df['date'],
                                                     open=filtered_df['open'],
                                                     high=filtered_df['high'],
                                                     low=filtered_df['low'],
                                                     close=filtered_df['close'])])
    fig_candlestick.update_layout(xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig_candlestick)

    # Volume Chart
    st.subheader("Bitcoin Trading Volume")
    fig_volume = px.bar(filtered_df, x='date', y='volume')
    st.plotly_chart(fig_volume)

with tab3:
    # Moving Averages
    st.subheader("Bitcoin Prices with Moving Averages")
    filtered_df['MA20'] = filtered_df['close'].rolling(window=20).mean()
    filtered_df['MA50'] = filtered_df['close'].rolling(window=50).mean()
    fig_ma = px.line(filtered_df, x='date', y=['close', 'MA20', 'MA50'])
    st.plotly_chart(fig_ma)

    # Statistical Summary
    st.subheader("Statistical Summary")
    st.write(filtered_df.describe())

    # Heatmap of Daily Returns
    st.subheader("Heatmap of Daily Returns")
    filtered_df['daily_return'] = filtered_df['close'].pct_change()
    daily_returns = filtered_df.pivot_table(index=filtered_df['date'].dt.year, columns=filtered_df['date'].dt.day, values='daily_return')
    fig_heatmap = px.imshow(daily_returns, labels=dict(x="Day", y="Year", color="Daily Return"))
    st.plotly_chart(fig_heatmap)

    # Sentiment Analysis (assuming you have a sentiment column)
    # st.subheader("Sentiment Over Time")
    # fig_sentiment = px.line(filtered_df, x='date', y='sentiment')
    # st.plotly_chart(fig_sentiment)

    # Correlation Matrix
    # Uncomment if sentiment data is available
    # st.subheader("Correlation Matrix")
    # correlation_matrix = filtered_df[['close', 'volume', 'sentiment']].corr()
    # fig_corr = px.imshow(correlation_matrix, text_auto=True)
    # st.plotly_chart(fig_corr)
