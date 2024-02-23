from dotenv import load_dotenv
import data_creation
import json
import os


# STEP 0: Create JSON files to access stock data and articles.

COMPANY_NAME = "Tesla Inc"

load_dotenv("/Users/alexdubro/.conda/.envs.txt")

# Tesla stock data

STOCK_SYMBOL = "TSLA"
STOCK_API_KEY = os.getenv('ALPHA_VANTAGE') # ALPHA_VANTAGE='7O19AT8N3E6M0PQ9' 'W9C6WQ9ILW136H0M' used to be the apikey
print(STOCK_API_KEY)

stock_endpoint = 'https://www.alphavantage.co/query'
stock_api_call = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_SYMBOL,
    'apikey': STOCK_API_KEY
}

# Create a Tesla stocks instance of DataHandler
stocks = data_creation.DataHandler(stock_endpoint, stock_api_call)

# Get stock data
stock_data = stocks.get_data()

# Load or create JSON using the method of the instance
stocks.load_or_create_json("stock_data.json", stock_data, formatting=4)


# Tesla articles

NEWS_COMPANY_NAME = "Tesla"
NEWS_API_KEY = os.getenv('NEWS_API') # NEWS_API='19f3705bd3ab41e7a2e5a69840086007'
print(NEWS_API_KEY)

endpoint_news = 'https://newsapi.org/v2/everything'
api_call_news = {
    'apiKey': NEWS_API_KEY,
    'q': NEWS_COMPANY_NAME,
    'language': 'en',
    'sortBy': 'relevancy',
    'pageSize': 3,
}

# Create a Tesla articles instance of DataHandler
tesla = data_creation.DataHandler(endpoint_news, api_call_news)

# Get the 3 most recent Tesla articles
tesla_articles = tesla.get_data()

# Load or create JSON using the method of the instance
tesla.load_or_create_json("tesla_articles.json", tesla_articles, formatting=4)