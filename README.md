# Bitcoin News and Price Sentiment Analysis

This project automates the process of fetching and storing Bitcoin price data, scraping Bitcoin-related news articles, analyzing their sentiment, and storing the results in a database. It leverages the AlphaVantage API for Bitcoin data, Hugging Face API for sentiment analysis, and a PostgreSQL database for storing the processed data. The main objective is to examine if the sentiment from news articles affects Bitcoin prices.

## Table of Contents

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Environment Variables](#environment-variables)
4. [Function Descriptions](#function-descriptions)
5. [Usage](#usage)
6. [Testing Locally](#testing-locally)
7. [Deployment](#deployment)
8. [Error Handling](#error-handling)
9. [License](#license)

## Introduction

This project automates the process of fetching Bitcoin price data, scraping Bitcoin-related news articles, analyzing their sentiment, and storing the results in a PostgreSQL database. It uses the AlphaVantage API for obtaining Bitcoin prices and the Hugging Face API for sentiment analysis of news articles. The goal is to analyze if the sentiment derived from the news articles has any correlation or impact on Bitcoin prices.

## Setup

To set up this project, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/bitcoin-news-sentiment-analysis.git
    cd bitcoin-news-sentiment-analysis
    ```

2. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the environment variables:**
    Create a `.env` file in the root directory of your project and add the required environment variables (described below).

## Environment Variables

This project requires the following environment variables:

- `Hugging_Token`: Your Hugging Face API token.
- `AlphaVantage_API_Key`: Your AlphaVantage API key.
- `DataBase_Url`: The connection string for your PostgreSQL database.

Example `.env` file:

## Function Descriptions

### `fetch_bitcoin_news`

This function scrapes Bitcoin-related news articles from the Financial Times website.

- **Input:** `event`, `context`
- **Output:** A JSON object containing the date and title of each news article.

### `lambda_handler` (Sentiment Analysis)

This function receives the scraped news articles, analyzes their sentiment using a pre-trained Hugging Face model, and returns the sentiment scores.

- **Input:** `event`, `context`
- **Output:** A JSON object containing the date, title, and sentiment scores (negative, positive, neutral) for each news article.

### `save_to_database`

This function saves the analyzed news articles to a PostgreSQL database.

- **Input:** A list of news articles with sentiment scores.
- **Output:** A status message indicating success or failure.

### `fetch_bitcoin_prices`

This function fetches the latest Bitcoin prices from the AlphaVantage API and stores the data in the database.

- **Input:** `event`, `context`
- **Output:** A status message indicating success or failure.

## Usage

1. **Fetch and Store Bitcoin Prices:**
    Call the `fetch_bitcoin_prices` function to fetch and store the latest Bitcoin prices in the database.

2. **Scrape News Articles:**
    Call the `fetch_bitcoin_news` function to scrape news articles from the Financial Times website.

3. **Analyze Sentiment:**
    Pass the scraped news articles to the `lambda_handler` function to analyze their sentiment.

4. **Save to Database:**
    Pass the sentiment-analyzed news articles to the `save_to_database` function to save them to the database.

## Testing Locally

To test the functions locally, you can use the following code snippets:

### Testing `fetch_bitcoin_news`
```python
if __name__ == "__main__":
    event = {}
    context = {}
    response = fetch_bitcoin_news(event, context)
    print(response['body'])
```
### Testing Sentiment Analysis and Database Save
```python
if __name__ == "__main__":
    event = {
        "responsePayload": {
            "body": [
                {
                    "date": "2024-06-10",
                    "title": "European bitcoin ETPs suffer mounting outflows"
                },
                {
                    "date": "2024-05-24",
                    "title": "British-Chinese bitcoin money launderer jailed for over 6 years"
                }
            ]
        }
    }
    context = {}
    sentiment_response = lambda_handler(event, context)
    print(sentiment_response['body'])

    # Assuming sentiment_response['body'] is a JSON string of processed news
    news_data = json.loads(sentiment_response['body'])
    save_response = save_to_database(news_data)
    print(save_response)
```
### Testing fetch_bitcoin_prices
```python
if __name__ == "__main__":
    event = {}
    context = {}
    price_response = fetch_bitcoin_prices(event, context)
    print(price_response)
```


## Deployment
To deploy this project as an AWS Lambda function:

1. Package the project files, including the .env file and dependencies.
2. Upload the package to AWS Lambda.
3. Set the environment variables in the AWS Lambda console.

## Error Handling
The project includes basic error handling for network requests and database operations. Errors are printed to the console and an appropriate status message is returned.

## License
This project is licensed under the MIT License. See the [LICENSE](License) file for details.


This README provides a comprehensive overview of your project, including setup instructions, function descriptions, usage examples, and deployment details, personalized to showcase your work on the project and its goal to analyze the correlation between news sentiment and Bitcoin prices.
