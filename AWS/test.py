import os
import psycopg2
import json

def save_bitcoin_data(data):
    Database_URL = os.getenv('DataBase_Url')
    
    
    conn = psycopg2.connect(Database_URL)
    cursor = conn.cursor()
        
     # Parse the incoming event
    #data = json.loads(data['body'])
        
    for date, values in data.items():
        cursor.execute('''
            INSERT INTO Bitcoin_Prices_Update(Date, Open, High, Low, Close, Volume)
            Values(%s, %s, %s, %s, %s, %s)
            ON CONFLICT (Date) DO NOTHING
          ''', (date, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. volume']))
        
    conn.commit()
    cursor.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
        }
  


data={
  "body": "{\"2025-06-04\": {\"1. open\": \"68791.04000000\", \"2. high\": \"68981.88000000\", \"3. low\": \"68640.03000000\", \"4. close\": \"68935.24000000\", \"5. volume\"}}"
}
save_bitcoin_data(data)