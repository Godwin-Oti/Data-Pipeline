import json
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv('DATABASE_URL')

def save_bitcoin_news(event, context):
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        
        # Parse the input data (assuming it's JSON)
        data = json.loads(event['body'])
        
        # Insert the Bitcoin news into the database
        try:
            cursor = conn.cursor()
            for item in data:
                cursor.execute('''
                    INSERT INTO Bitcoin_News_Update (id, date, title)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                ''', (item['id'], item['date'], item['title']))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f'Error inserting Bitcoin data: {e}')
            conn.rollback()
        
        # Close the connection
        conn.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data inserted successfully')
        }
    except Exception as e:
        print(f'Error in save_bitcoin_news: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e}')
        }
