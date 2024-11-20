from dotenv import load_dotenv
import data_creation
import json
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def get_input(prompt):
    user_input = input(prompt)
    driver = webdriver.Chrome()
    driver.get("https://stockanalysis.com/stocks/")

    search_input = driver.find_element(By.XPATH, "/html/body/div[2]/header/div/div[1]/form/div/input")
    search_input.send_keys(user_input)

    # Wait for search results to load (adjust sleep time as needed)
    time.sleep(5)

    # Check if there are no results
    if "No results. Try modifying your query." in driver.page_source:
        result = "No results. Try modifying your query."
    else:
        symbols = []
        elements = driver.find_elements(By.CLASS_NAME, "svelte-1jtwn20")
        for element in elements:
            symbols.append(element.text)
        result = symbols  # or any other result you want to return

    driver.quit()  # Close the WebDriver instance
    return result

# Example usage:
company_info = get_input("Please provide the company's name, e.g. Tesla, Inc, or its stock symbol, e.g. TSLA: ")
print(company_info)

# COMPANY_NAME = 
# STOCK_SYMBOL = 

# # STEP 0: Create JSON files to access stock data and articles.

# load_dotenv("/Users/alexdubro/.conda/.envs.txt")

# # Stock data

# STOCK_API_KEY = os.getenv('ALPHA_VANTAGE')


# stock_endpoint = 'https://www.alphavantage.co/query'
# stock_api_call = {
#     'function': 'TIME_SERIES_DAILY',
#     'symbol': STOCK_SYMBOL,
#     'apikey': STOCK_API_KEY
# }

# # Create a Tesla stocks instance of DataHandler
# stocks = data_creation.DataHandler(stock_endpoint, stock_api_call)

# # Get stock data
# stock_data = stocks.get_data()

# # Load or create JSON using the method of the instance
# stocks.load_or_create_json("stock_data.json", stock_data, formatting=4)


# # שׁrticles

# NEWS_API_KEY = os.getenv('NEWS_API')


# endpoint_news = 'https://newsapi.org/v2/everything'
# api_call_news = {
#     'apiKey': NEWS_API_KEY,
#     'q': COMPANY_NAME,
#     'language': 'en',
#     'sortBy': 'relevancy',
# }

# # Create a Tesla articles instance of DataHandler
# tesla = data_creation.DataHandler(endpoint_news, api_call_news)

# # Get the 3 most recent Tesla articles
# tesla_articles = tesla.get_data()

# # Load or create JSON using the method of the instance
# tesla.load_or_create_json("articles.json", articles, formatting=4)