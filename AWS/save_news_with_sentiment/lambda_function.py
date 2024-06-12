import json
import os
import psycopg2

# Database connection parameters
DATABASE_URL = os.getenv('DATABASE_URL')

def save_to_database(news_data):
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        
        # Insert the Bitcoin news into the database
        cursor = conn.cursor()
        for item in news_data:
            cursor.execute('''
                INSERT INTO sentiment_bitcoin_news (date, title, negative, positive, neutral)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT(title) DO NOTHING
            ''', (item['date'], item['title'], item['negative'], item['positive'], item['neutral']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data inserted successfully')
        }
    except Exception as e:
        print(f'Error inserting Bitcoin data: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error inserting Bitcoin data: {e}')
        }

def lambda_handler(event, context):
    news_data = json.loads(event['body'])
    return save_to_database(news_data)

# For local testing
#if __name__ == "__main__":
    #event = {
        #"body": json.dumps([
            #{
                #"date": "2024-06-10",
                #"title": "European bitcoin ETPs suffer mounting outflows",
                #"negative": 0.85,
                #"positive": 0.1,
                #"neutral": 0.05
            #},
            #{
               ## "date": "2024-06-11",
                #"title": "Bitcoin price surges after regulatory approval",
                #"negative": 0.1,
                #"positive": 0.85,
                #"neutral": 0.05
            #},
            #{
                #"date": "2024-06-12",
                #"title": "Cryptocurrency market experiences significant downturn",
                #"negative": 0.78,
                #"positive": 0.15,
                #"neutral": 0.07
            #}
        #])
    #}
    #context = {}
    #result = lambda_handler(event, context)
    #print(result)
