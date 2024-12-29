from dotenv import load_dotenv
import data_creation
import json
import os

"""
All company names and stock symbols can be found on this website:
https://stockanalysis.com/

Before running this script, please find yours there.

Here, I will be using Tesla.

Additionally, please get an API key from Alpha Vantage and News API. I'm accessing mine via environmental variables.
"""

# STEP 1: Specify company name and stock symbol.  

# Example: Tesla 
# https://stockanalysis.com/symbol-lookup/?q=tesla

COMPANY_NAME = input("What is the company name? ") # "Tesla Inc"
STOCK_SYMBOL = input("What is the company's stock symbol? ") # "TSLA"

# STEP 2: Create JSON files to access (1) stock data and (2) articles.

load_dotenv("/Users/alexdubro/.conda/.envs.txt")

# 2.1) Tesla stock data

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

# 2.2) Tesla articles

NEWS_API_KEY = os.getenv('NEWS_API')

endpoint_news = 'https://newsapi.org/v2/everything'
api_call_news = {
    'apiKey': NEWS_API_KEY,
    'q': COMPANY_NAME,
    'language': 'en',
    'sortBy': 'relevancy',
}

# Create a Tesla articles instance of DataHandler
articles = data_creation.DataHandler(endpoint_news, api_call_news)

# Get the 3 most recent Tesla articles
news_articles = articles.get_data()

# Load or create JSON using the method of the instance
articles.load_or_create_json("news_articles.json", news_articles, formatting=4)