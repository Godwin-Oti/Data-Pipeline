import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def get_bitcoin_news(last_page=72):
    # URL of the webpage to scrape
    base_url = 'https://www.ft.com/bitcoin?page='

    # Create lists to store extracted data
    headlines_list = []
    subheadlines_list = []
    dates_list = []

    # Calculate the cutoff date (180 days ago from today)
    cutoff_date = datetime.now() - timedelta(days=180)

    for page in range(1, last_page+1):
        # Construct the URL for the current page
        url = base_url + str(page)

        # Send an HTTP request to the webpage
        res = requests.get(url)

        # Check if the request was successful
        if res.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Find all headlines related to Bitcoin
            headlines = soup.select('.o-teaser__heading')
            subheadlines = soup.select('.js-teaser-standfirst-link')
            dates = soup.select('.o-date')

            # Iterate over each headline, subheadline, and date
            for headline, subheadline, date in zip(headlines, subheadlines, dates):
                # Extract the text from the headline, subheadline, and date elements
                headline_text = headline.text.strip()
                subheadline_text = subheadline.text.strip()
                date_text = date.text.strip()

                # Parse the date string
                date_obj = datetime.strptime(date_text, "%A, %d %B, %Y")

                # Check if the article is within the cutoff date
                if date_obj >= cutoff_date:
                    # Append the extracted data to lists
                    headlines_list.append(headline_text)
                    subheadlines_list.append(subheadline_text)
                    dates_list.append(date_obj)
        else:
            print(f"Failed to retrieve the page {page}. Status code: {res.status_code}")

    # Create DataFrame from the lists
    df = pd.DataFrame({'date': dates_list, 'headline': headlines_list, 'subheadline': subheadlines_list})

    # Sort DataFrame by 'Date'
    df = df.sort_values(by='date')

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df

# Usage
bitcoin_headlines_df = get_bitcoin_news(last_page=72)

# Print the DataFrame
if bitcoin_headlines_df is not None:
    print(bitcoin_headlines_df)