from datetime import datetime
from dotenv import load_dotenv
import json
import os
import time
from twilio.rest import Client


# STEPS 1 & 2: 
#   1: When STOCK price increase/decreases by 5% between yesterday and the day before yesterday, then print("Get News")
#   2: Use https://newsapi.org to provide additional information about the company, date, stock value, and percentage change


# Access the JSON stock data and articles

start = time.perf_counter()

with open('stock_data.json', 'r') as stock_file, open('news_articles.json', 'r') as articles_file:
    stock_data = json.load(stock_file)
    article_data = json.load(articles_file)


# Stock data, with stock dates

time_series_daily = stock_data['Time Series (Daily)']
sorted_data = [(date, float(time_series_daily[date]['3. low'])) for date in time_series_daily]

stock_dates = {}

for i in range(2, len(sorted_data)):
    current_date, current_low = sorted_data[i]
    yesterday_date, yesterday_low = sorted_data[i - 1]
    two_days_ago_date, two_days_ago_low = sorted_data[i - 2]

    percentage_change = round(((yesterday_low - two_days_ago_low) / two_days_ago_low) * 100, 2)

    if percentage_change > 5 or percentage_change < -5:
        stock_dates[current_date] = percentage_change

# Articles

articles = article_data["articles"]

# Reformat the articles in a dictionary with a datetime publication date and other properties
formatted_article_data = {}

for article in articles:
    publication_date = datetime.fromisoformat(article["publishedAt"][:-1]).strftime("%Y-%m-%d")
    if publication_date not in formatted_article_data:
        formatted_article_data[publication_date] = []
    formatted_article_data[publication_date].append({
        "source": article["source"]["name"],
        "author": article["author"],
        "title": article["title"],
        "publication_date": publication_date,
        "content": article["content"]
    })


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

for date in stock_dates:
    if date in formatted_article_data:
        # print(f'Get news! Look at the stock value: {date}: {yesterday_low}. It changed by {stock_dates[date]}%.')
        articles_for_date = formatted_article_data[date]
        for article in articles_for_date:
            message_title = article["title"]
            message_author = article['author']
            message_content = article["content"]
            message_source = f'This content comes to you from {article["source"]}!'

# Access the environmental variables

env_path = input("What is your environmental path? ")

load_dotenv(f"/Users/{env_path}/.conda/.envs.txt")
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

send_to = int(input("What phone number would you like to send to? "))
with open("stock_symbol.txt", "r") as file:
    STOCK_SYMBOL = file.read().strip()

message = client.messages.create(
    body=f'{STOCK_SYMBOL}: 🔺{stock_dates[date]}%\nHeadline: {message_title}\n{message_author}\nBrief: {message_content}\n{message_source}',
    from_=TWILIO_PHONE_NUMBER,
    to=send_to
)

end = time.perf_counter()
execution_time = end - start # How long the program takes to run

# Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.

TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""