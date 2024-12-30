from dotenv import load_dotenv
import data_creation
import json
import os

# STEP 1: Identify the company's stock and stock symbol.

"""
You can identify the company name and stock symbol on this website:
https://stockanalysis.com/

You will need an API key on Alpha Vantage and News API, too.
"""

# COMPANY_NAME = input('What is the company\'s name? ') # Tesla Inc
# STOCK_SYMBOL = input('What is the company\'s stock symbol? ') #TSLA

# # STEP 2: Create JSON files to access stock data and articles.

# env_path = input("What is your environmental path? ")

# load_dotenv(f"/Users/{env_path}/.conda/.envs.txt") # alexdubro

# # 2.1) Stock data

# STOCK_API_KEY = os.getenv('ALPHA_VANTAGE')

# stock_endpoint = 'https://www.alphavantage.co/query'
# stock_api_call = {
#     'function': 'TIME_SERIES_DAILY',
#     'symbol': STOCK_SYMBOL,
#     'apikey': STOCK_API_KEY
# }

# # 2.2) Articles

# NEWS_API_KEY = os.getenv('NEWS_API')

# endpoint_news = 'https://newsapi.org/v2/everything'
# api_call_news = {
#     'apiKey': NEWS_API_KEY,
#     'q': COMPANY_NAME,
#     'language': 'en',
#     'sortBy': 'relevancy',
# # }
# STOCK_SYMBOL = input('What is the company\'s stock symbol? ') #TSLA

# if __name__ == "__main__":

#     COMPANY_NAME = input('What is the company\'s name? ') # Tesla Inc
#     # STOCK_SYMBOL = input('What is the company\'s stock symbol? ') #TSLA

#     # STEP 2: Create JSON files to access stock data and articles.

#     env_path = input("What is your environmental path? ")

#     load_dotenv(f"/Users/{env_path}/.conda/.envs.txt") # alexdubro

#     # 2.1) Stock data

#     STOCK_API_KEY = os.getenv('ALPHA_VANTAGE')

#     stock_endpoint = 'https://www.alphavantage.co/query'
#     stock_api_call = {
#         'function': 'TIME_SERIES_DAILY',
#         'symbol': STOCK_SYMBOL,
#         'apikey': STOCK_API_KEY
#     }

#     # 2.2) Articles

#     NEWS_API_KEY = os.getenv('NEWS_API')

#     endpoint_news = 'https://newsapi.org/v2/everything'
#     api_call_news = {
#         'apiKey': NEWS_API_KEY,
#         'q': COMPANY_NAME,
#         'language': 'en',
#         'sortBy': 'relevancy',
#     }

#     # Create a stocks instance of DataHandler
#     stocks = data_creation.DataHandler(stock_endpoint, stock_api_call)
#     stock_data = stocks.get_data()
#     stocks.load_or_create_json("stock_data.json", stock_data, formatting=4)

#     # Create a news articles instance of DataHandler
#     articles = data_creation.DataHandler(endpoint_news, api_call_news)
#     news_articles = articles.get_data()
#     articles.load_or_create_json("news_articles.json", news_articles, formatting=4)


# create_json.py

STOCK_SYMBOL = None

if __name__ == "__main__":
    STOCK_SYMBOL = input("What is the company's stock symbol? ")  # TSLA
    # Inside the `if __name__ == "__main__":` block
    with open("stock_symbol.txt", "w") as file:
        file.write(STOCK_SYMBOL)

    COMPANY_NAME = input("What is the company's name? ")  # Tesla Inc

    # STEP 2: Create JSON files to access stock data and articles.
    env_path = input("What is your environmental path? ")

    load_dotenv(f"/Users/{env_path}/.conda/.envs.txt")  # alexdubro

    # 2.1) Stock data
    STOCK_API_KEY = os.getenv('ALPHA_VANTAGE')
    stock_endpoint = 'https://www.alphavantage.co/query'
    stock_api_call = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': STOCK_SYMBOL,
        'apikey': STOCK_API_KEY
    }

    # 2.2) Articles
    NEWS_API_KEY = os.getenv('NEWS_API')
    endpoint_news = 'https://newsapi.org/v2/everything'
    api_call_news = {
        'apiKey': NEWS_API_KEY,
        'q': COMPANY_NAME,
        'language': 'en',
        'sortBy': 'relevancy',
    }

    # Create a stocks instance of DataHandler
    stocks = data_creation.DataHandler(stock_endpoint, stock_api_call)
    stock_data = stocks.get_data()
    stocks.load_or_create_json("stock_data.json", stock_data, formatting=4)

    # Create a news articles instance of DataHandler
    articles = data_creation.DataHandler(endpoint_news, api_call_news)
    news_articles = articles.get_data()
    articles.load_or_create_json("news_articles.json", news_articles, formatting=4)
