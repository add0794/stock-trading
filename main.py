from create_json import STOCK_SYMBOL
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import os
import re
from timeit import default_timer as timer
from twilio.rest import Client


# STEPS 1 & 2: 
#   1: When STOCK price increase/decreases by 5% between yesterday and the day before yesterday, then print("Get News")
#   2: Use https://newsapi.org to provide additional information about the company, date, stock value, and percentage change


# Access the JSON stock data and articles

start = timer() # Keep track of execution time

with open('stock_data.json', 'r') as stock_file, open('articles.json', 'r') as articles_file:
    stock_data = json.load(stock_file)
    article_data = json.load(articles_file)


# 1) Stock data

# Create a user input that asks until you enter a correct input

def get_input(prompt, input_type): 
    while True:
        try:
            if prompt == "What phone number would you like to send to? ":
                print("Please enter your phone number with the international area code and the 10-digit phone number, with no spaces or dashes between the numbers.\nExample: +18552735462\nTwilio's Terms of Service apply for international numbers.")

            user_input = input(prompt)
            
            if input_type == float:
                user_input = re.sub(r'[^0-9.]', '', user_input)
                result = round(input_type(user_input), 3)
                return result
            elif input_type == str and prompt == "What phone number would you like to send to?":
                result = "+" + re.sub(r'\D', '', user_input)  # Keep only digits after the +
                return result
            else:
                return input_type(user_input)  # return the input if it's string

        except (TypeError, ValueError):
            print("Invalid input. Please try again.") # Catch any errors and prompt the question again

percentage_change_threshold = get_input("What percentage change matters to you? ", float) # Percentage change threshold by which all (absolute) percentage changes should be greater or equal to


time_series_daily = stock_data['Time Series (Daily)']
sorted_data = [(date, float(time_series_daily[date]['3. low'])) for date in time_series_daily] # List comprehension of tuples of dates and stock data 


stock_dates = {} # Dictionary with dates and percentage changes meeting that threshold

for i in range(2, len(sorted_data)):
    current_date, current_low = sorted_data[i]
    yesterday_date, yesterday_low = sorted_data[i - 1]
    two_days_ago_date, two_days_ago_low = sorted_data[i - 2]

    percentage_change = abs(round(((yesterday_low - two_days_ago_low) / two_days_ago_low) * 100, 2))
    
    if percentage_change > percentage_change_threshold:
        stock_dates[current_date] = percentage_change


# 2) Articles

articles = article_data["articles"]

formatted_article_data = {} # Nested dictionary with a datetime publication date as the opening key showing source, author, title, and content

for article in articles:
    publication_date = datetime.fromisoformat(article["publishedAt"][:-1]).strftime("%Y-%m-%d")
    if publication_date not in formatted_article_data:
        formatted_article_data[publication_date] = {}
        formatted_article_data[publication_date]["source"] = article["source"]["name"]
        formatted_article_data[publication_date]["author"] = article["author"]
        formatted_article_data[publication_date]["title"] = article["title"]
        formatted_article_data[publication_date]["content"] = article["content"]
print(formatted_article_data)

## STEP 3: Use https://www.twilio.com
# Send a formatted message to a specified phone number if a stock date reaches that percentage change threshold. 

for date in stock_dates: 
    if date in formatted_article_data: # Checking for the stock percentage change dates in formatted_article_data
        for sorted_date, low_value in sorted_data: # Getting the stock value on those dates
            if sorted_date == date:
                print(f'Get news! Look at the stock value: {date}: {low_value}. It changed by {stock_dates[date]}%.') # Showing the dates, stock values, and percentage changes for those dates before messaging via Twilio
                for date in formatted_article_data[date]:
                    message_title = date["title"]
                    message_author = date['author']
                    message_content = date["content"]
                    message_source = f'This content comes to you from {date["source"]["name"]}!'


# Access Twilio environment variables

load_dotenv("/Users/alexdubro/.conda/.envs.txt")
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Message to specified number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

send_to = get_input("What phone number would you like to send to? ", str)

message = client.messages.create(
    body=f'{STOCK_SYMBOL}: 🔺{stock_dates[date]}%\nHeadline: {message_title}\n{message_author}\nBrief: {message_content}\n{message_source}',
    from_=TWILIO_PHONE_NUMBER,
    to=send_to
)

# Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.

TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


# Execution time

end = timer()
execution_time = timedelta(seconds=end-start)
print(f'This program took {execution_time}.') # How long the program takes to run
