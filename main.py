import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api = "ec383f5353b945c1babc6b66a6b7037b"
alpha_api_key = 'TAS87OBN4Z51E68S'
alpha_paramaters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': alpha_api_key
}
paramaters = {
    'q': COMPANY_NAME,
    'apiKey': api
}
twillo_sid = 'ACd5857045c8cbb5f8229fa6fe83ce0816'
twillo_token ='611ee57495b0cf72c6f825824ccf25cf'
twillo_phone_number = '+19164720348'



## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 
a = requests.get(url=STOCK_ENDPOINT,params=alpha_paramaters)
a.raise_for_status()
stock_price = a.json()['Time Series (Daily)']
stock_price_dict = [value for (key, value) in stock_price.items()]
yesterday = stock_price_dict[0]
yesterdays_close_price = yesterday['4. close']

day_before_data = stock_price_dict[1]
day_before_close_price = day_before_data['4. close']

diff = float(yesterdays_close_price)-float(day_before_close_price)
up_down = None
if diff > 0:
    up_down = '🔺'
else:
    up_down = '🔻'



diff_percent = (diff / float(yesterdays_close_price))*100



## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
r = requests.get(url=NEWS_ENDPOINT, params=paramaters)
r.raise_for_status()
articles = r.json()['articles']
three_articles = articles[:3]
formatted = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted)
if diff_percent < 5:
    client = Client(twillo_sid, twillo_token)
    message = client.messages \
        .create(
        body=f"{formatted}",
        from_=twillo_phone_number,
        to='phone_number'
    )



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.




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

