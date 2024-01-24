import data_creation
import json


# STEP 0: Create JSON files to access stock data and articles.

COMPANY_NAME = "Tesla Inc"

# Tesla stock data

STOCK_SYMBOL = "TSLA"
STOCK_API_KEY = '7O19AT8N3E6M0PQ9' # 'W9C6WQ9ILW136H0M' used to be the apikey

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
NEWS_API_KEY = '19f3705bd3ab41e7a2e5a69840086007'

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


# STEP 1: When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

with open('stock_data.json', 'r') as json_file:
    data = json.load(json_file)

# sorted_data = [data["Time Series (Daily)"] for date in data["Time Series (Daily)"]]
time_series_daily = data['Time Series (Daily)']
sorted_data = [
    (date, float(time_series_daily[date]['3. low']))
    for date in time_series_daily
]

stock_dates = []

for i in range(2, len(sorted_data)):
    current_date, current_low = sorted_data[i]
    yesterday_date, yesterday_low = sorted_data[i - 1]
    two_days_ago_date, two_days_ago_low = sorted_data[i - 2]

    percentage_change = round(((yesterday_low - two_days_ago_low) / two_days_ago_low) * 100, 2)

    if percentage_change > 5 or percentage_change < -5:
        print(f'Get news! Look at the stock value: {yesterday_date}: {yesterday_low}. It changed by {percentage_change}%.')
        stock_dates.append(yesterday_date)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

with open('tesla_articles.json', 'r') as json_file:
    articles = json.load(json_file)

for article in articles["articles"]:
    print(article["description"])


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['AC9de9f16ce7652cfa25c559bc8fc09f85']
# auth_token = os.environ['62f21542f0555ab92c7371e9a706de64']
# client = Client(account_sid, auth_token)

print(f'{STOCK_SYMBOL}: {percentage_change}')

# message = client.messages.create(
#                               from_='+15017122661',
#                               body='Hi there',
#                               to='+15558675310'
#                           )

# print(message.sid)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

