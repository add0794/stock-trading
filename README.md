# Stock Trading with Public Companies

It can be very time-consuming to follow a company's stock value, but you still want to earn a little extra income from investing in your favorite public company.

No more!

This program not only tracks changes in its stock value; it automatically texts you when a significant change happens (e.g. 5%). When you set the percentage change, JSON files are created for each day for the last few months:

1. Open
2. High
3. Low
4. Close
5. Volume

This program uses Tesla and generates its data in two separate JSON files. However, you can generate JSON files with stock data and relevant articles for any public company. 

Run create_json.py to generate the necessary JSON data. First, identify the company name and stock symbol [here](https://stockanalysis.com/).

You will need an API key on Alpha Vantage and News API, too.

Then, when you run main.py, you'll get updates straight to your phone. (Make sure to set yourself on [Twilio](https://www.twilio.com/en-us), too.)

Make your investing life easier, and perhaps, stop using a certified financial analyst (CFA) to do the dirty work.