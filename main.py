import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "BBWQUTZTY66EEABN"
NEWS_API_KEY = "35fe0f7b16934ea49179f650da4204a3"
TWILIO_SID = "AC2252020cbdb8c6c739bf37cdcea4ea4a"
TWILIO_AUTH_TOKEN = "988c7004abd91df48bda9410fafb3951"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

diff_percentage = (difference / float(yesterday_closing_price)) * 100

if diff_percentage > 3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()["articles"]
    three_article = articles[:3]

    formatted_article = [f"Headline {article['title']}. /nBrief: {article['description']}" for article in articles]

    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_="+17626752684",
            to="your mobile number"
        )

