import requests
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import pandas as pd
from Bitcoin_api import fetch_bitcoin_data
from new_scrappy import get_bitcoin_news

#1. Cennecting to Database and creating Tables
# make sure to load dotenv
load_dotenv()

# Database connection paramete(s
Database_URL = os.getenv('DataBase_Url')

#connect to database
conn = psycopg2.connect(Database_URL)
cur = conn.cursor()

#create tables if they don't exist

cur.execute('''
CREATE TABLE IF NOT EXISTS Bitcoin_Prices_Update(
    Date DATE PRIMARY KEY,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume FLOAT
    
)            
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Bitcoin_News_Update(
    id SERIAL PRIMARY KEY,
    date DATE,
    title VARCHAR(500)
       
)            
''')

conn.commit()

#2# Insertion of BTC prices

#function to insert Bitcoin_Prices
def insert_bitcoin_data(conn, data):
    try:
        cursor = conn.cursor()
        for index, row in data.iterrows():
            cursor.execute('''
                INSERT INTO Bitcoin_Prices_Update(Date, Open, High, Low, Close, Volume)
                Values(%s, %s, %s, %s, %s, %s)
                ON CONFLICT (Date) DO NOTHING
                ''',(index, row['1. Open'], row['2. High'], row['3. Low'], row['4. Close'], row['5. Volume']))
        conn.commit()
        cursor.close()
        print("success")
    except Exception as e:
        print(f'Error inserting Bitcoin data: {e}')
        conn.rollback()

#3# Insertion of BTC news

#function to insert Bitcoin_News
def insert_bitcoin_news(conn, df):
    try:
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute('''
                INSERT INTO Bitcoin_News_Update (id, date, title)
                Values(%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                ''',(index,row['date'], row['title']))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f'Error inserting Bitcoin data: {e}')
        conn.rollback()

#4# Fetching and inserting Data

#Main Function to orchestrate the data fetching and insertion
def main():
    # fetch Bitcoin Data
    bitcoin_data = fetch_bitcoin_data("BTC","USD")
    #Scrape Bitcoin News data
    bitcoin_titles_df = get_bitcoin_news()
    #connect to postgresSQL database
    conn = psycopg2.connect(Database_URL)

    if conn:
        #Insert data into database
        insert_bitcoin_data(conn,bitcoin_data)
        insert_bitcoin_news(conn,bitcoin_titles_df)

        #close the database connection
        conn.close()
    else:
        print('Failed to connect to the database')

if __name__== '__main__':
    main()