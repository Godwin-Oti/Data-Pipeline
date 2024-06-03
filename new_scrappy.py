import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def get_bitcoin_news():
    # URL of the webpage to scrape
    base_url = 'https://www.ft.com/bitcoin?page='

    # Create lists to store extracted data
    titles_list = []
    dates_list = []

    # Calculate the cutoff date (180 days ago from today)
    cutoff_date = datetime.now() - timedelta(days=180)

    page = 1
    while True:
        # Construct the URL for the current page
        url = base_url + str(page)

        # Send an HTTP request to the webpage
        res = requests.get(url)

        # Check if the request was successful
        if res.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Find all titles and dates related to Bitcoin
            titles = soup.select('.o-teaser__heading')
            dates = soup.select('.o-date')

            # If no titles or dates are found, break the loop
            if not titles or not dates:
                break

            # Temporary lists to store the current page's data
            current_titles_list = []
            current_dates_list = []

            # Iterate over each title and date
            for title, date in zip(titles, dates):
                # Extract the text from the title and date elements
                title_text = title.text.strip()
                date_text = date.text.strip()

                # Parse the date string
                try:
                    date_obj = datetime.strptime(date_text, "%A, %d %B, %Y")
                except ValueError:
                    continue  # Skip if date format is not as expected

                # Check if the article is within the cutoff date
                if date_obj >= cutoff_date:
                    # Append the extracted data to temporary lists
                    current_titles_list.append(title_text)
                    current_dates_list.append(date_obj)

            # Check if the current page's data is the same as the previous page's data
            if current_titles_list == titles_list[-len(current_titles_list):] and current_dates_list == dates_list[-len(current_dates_list):]:
                break

            # Append the current page's data to the main lists
            titles_list.extend(current_titles_list)
            dates_list.extend(current_dates_list)

            # Move to the next page
            page += 1
        else:
            print(f"Failed to retrieve the page {page}. Status code: {res.status_code}")
            break

    # Create DataFrame from the lists
    df = pd.DataFrame({'date': dates_list, 'title': titles_list})

    # Sort DataFrame by 'Date' in descending order
    df = df.sort_values(by='date', ascending=False)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df

# Usage
bitcoin_titles_df = get_bitcoin_news()

# Print the DataFrame
if bitcoin_titles_df is not None:
    print(bitcoin_titles_df)
