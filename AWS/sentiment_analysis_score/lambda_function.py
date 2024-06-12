import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

API_TOKEN = os.getenv('Hugging_Token')
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def analyze_sentiment(news_title):
    response = query({"inputs": news_title})
    if response and isinstance(response, list) and len(response) > 0:
        sentiments = {item['label']: item['score'] for item in response}
        return sentiments
    return None

def lambda_handler(event, context):
    news_data = json.loads(event['body'])
    processed_news = []

    for news in news_data:
        sentiment = analyze_sentiment(news["title"])
        if sentiment:
            processed_news.append({
                "date": news["date"],
                "title": news["title"],
                "negative": sentiment.get('negative', 0),
                "positive": sentiment.get('positive', 0),
                "neutral": sentiment.get('neutral', 0)
            })

    return {
        'statusCode': 200,
        'body': json.dumps(processed_news)
    }

# For local testing
#if __name__ == "__main__":
    #event = {
        #"body": json.dumps([
            #{"date": "2024-06-10", "title": "European bitcoin ETPs suffer mounting outflows"},
            #{"date": "2024-06-11", "title": "Bitcoin price surges after regulatory approval"},
            #{"date": "2024-06-12", "title": "Cryptocurrency market experiences significant downturn"}
        #])
    #}
    #context = {}
    #result = lambda_handler(event, context)
    #print(result)
