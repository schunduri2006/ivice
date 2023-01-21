import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import os
import openai
from flask import Flask, render_template

openai.api_key = "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"

def get_news_articles(ticker):
    API_KEY = "1e58693bc6d44c919b2b980ff4d3f0c0"
    url = "https://newsapi.org/v2/everything?q={}&apiKey={}".format(ticker, API_KEY)


    response = requests.get(url)
    data = json.loads(response.text)
    articles = data["articles"]

   
    articles_list = []
    for article in articles:
        headline = article["title"]
        url = article["url"]
        content = article["content"]
        articles_list.append({"headline": headline, "url": url, "content": content})


    df = pd.DataFrame(articles_list)
    return df

df = get_news_articles("AAPL")
print(df.head())


df = df.head()
summary_list = []

for i, row in df.iterrows():
    content = row['content']
    if content is not None:
        response = openai.Completion.create(
            engine="text-ada-001",
            prompt=(f"Please summarize the text's opinion about Apple stock using {content}"),
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5)
        summary = response["choices"][0]["text"]
        print(summary)
        summary_list.append({"summary": summary})
    else:
        print("No summary available")

df1 = pd.DataFrame(summary_list)
df1


response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=(f"Summarize the future of Apple stock and suggest to buy,sell, or hold the stock using the following information: {df1}"),
    max_tokens = 500,
    n=1,
    stop=None,
    temperature=0.5
)
fullsummary = response["choices"][0]["text"]


print("BREAK")
text = fullsummary
lines = text.split("\n")
for i, line in enumerate(lines):
    if i % 2 == 0:
        print("    " + line)
    else:
        print(line)

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        df = get_news_articles("AAPL")
        df1 = pd.DataFrame(summary_list)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(f"Summarize the future of Apple stock and suggest to buy,sell, or hold the stock using the following information: {df1}"),
            max_tokens = 500,
            n=1,
            stop=None,
            temperature=0.5
        )
        fullsummary = response["choices"][0]["text"]
        return render_template('index.html', fullsummary=fullsummary)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

