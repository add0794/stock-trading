from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os
import requests
import json
import data_creation  # Assuming this module is available

# Load environment variables
load_dotenv("/Users/alexdubro/.conda/.envs.txt")

STOCK_API_KEY = os.getenv('ALPHA_VANTAGE')
NEWS_API_KEY = os.getenv('NEWS_API')

# Function to fetch stock symbols using Selenium
def fetch_stock_symbols(prompt):
    """Fetch stock symbols dynamically from stockanalysis.com based on user input."""
    user_input = input(prompt)
    driver = webdriver.Chrome()
    driver.get("https://stockanalysis.com/stocks/")

    # Input the search term
    search_input = driver.find_element(By.XPATH, "/html/body/div[2]/header/div/div[1]/form/div/input")
    search_input.send_keys(user_input)
    time.sleep(5)  # Wait for results to load

    # Check results
    elements = driver.find_elements(By.CLASS_NAME, "svelte-1jtwn20")
    symbols = [element.text for element in elements] if elements else []

    driver.quit()
    return symbols if symbols else None

# Function to fetch stock data
def fetch_stock_data(symbol):
    """Fetch stock data using Alpha Vantage API."""
    stock_endpoint = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': STOCK_API_KEY
    }
    response = requests.get(stock_endpoint, params=params)
    response.raise_for_status()
    return response.json()

# Function to fetch news articles
def fetch_news(company_name):
    """Fetch news articles using NewsAPI."""
    endpoint_news = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': NEWS_API_KEY,
        'q': company_name,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 3
    }
    response = requests.get(endpoint_news, params=params)
    response.raise_for_status()
    return response.json()

# Function to save data as JSON
def save_json(file_name, data):
    """Save data to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Main function
def main():
    # Step 1: Get stock symbols dynamically
    stock_symbols = fetch_stock_symbols("Enter a company name or stock symbol: ")

    if not stock_symbols:
        print("No stock symbols found. Exiting.")
        return

    # Use the first stock symbol (or prompt user to choose one)
    STOCK_SYMBOL = stock_symbols[0]  # Default to the first result
    print(f"Using stock symbol: {STOCK_SYMBOL}")

    # Ask for the company name (for fetching news)
    COMPANY_NAME = input("Enter the company's full name (e.g., Tesla, Inc.): ")

    # Step 2: Fetch and save stock data
    print("Fetching stock data...")
    stock_data = fetch_stock_data(STOCK_SYMBOL)
    stock_file_name = f"stock_data_{STOCK_SYMBOL}.json"
    save_json(stock_file_name, stock_data)
    print(f"Stock data saved to {stock_file_name}")

    # Step 3: Fetch and save news articles
    print("Fetching news articles...")
    news_data = fetch_news(COMPANY_NAME)
    news_file_name = f"articles_{COMPANY_NAME.replace(' ', '_')}.json"
    save_json(news_file_name, news_data)
    print(f"News articles saved to {news_file_name}")

main()