from dotenv import load_dotenv
import data_creation
import json
import os


# STEP 0: Create JSON files to access stock data and articles.

COMPANY_NAME = "Tesla Inc"

load_dotenv("/Users/alexdubro/.conda/.envs.txt")

# Tesla stock data

STOCK_SYMBOL = "TSLA"
STOCK_API_KEY = os.getenv('ALPHA_VANTAGE')


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
NEWS_API_KEY = os.getenv('NEWS_API')


endpoint_news = 'https://newsapi.org/v2/everything'
api_call_news = {
    'apiKey': NEWS_API_KEY,
    'q': NEWS_COMPANY_NAME,
    'language': 'en',
    'sortBy': 'relevancy',
}

# Create a Tesla articles instance of DataHandler
tesla = data_creation.DataHandler(endpoint_news, api_call_news)

# Get the 3 most recent Tesla articles
tesla_articles = tesla.get_data()

# Load or create JSON using the method of the instance
tesla.load_or_create_json("tesla_articles.json", tesla_articles, formatting=4)