import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def fetch_bitcoin_news(event, context):
    base_url = 'https://www.ft.com/bitcoin?page='
    titles_list = []
    dates_list = []
    cutoff_date = datetime.now() - timedelta(days=180)
    page = 1

    while True:
        url = base_url + str(page)
        res = requests.get(url)

        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('.o-teaser__heading')
        dates = soup.select('.o-date')

        if not titles or not dates:
            break

        for title, date in zip(titles, dates):
            title_text = title.text.strip()
            date_text = date.text.strip()

            try:
                date_obj = datetime.strptime(date_text, "%A, %d %B, %Y")
            except ValueError:
                continue

            if date_obj >= cutoff_date:
                titles_list.append(title_text)
                dates_list.append(date_obj)

        page += 1

    news_data = [{'date': date.strftime('%Y-%m-%d'), 'title': title} for date, title in zip(dates_list, titles_list)]
    
    return {
        'statusCode': 200,
        'body': json.dumps(news_data)
    }

# This section is for testing the function locally
#if __name__ == "__main__":
    #event = {}
    #context = {}
    #response = fetch_bitcoin_news(event, context)
    #print(response['body'])
