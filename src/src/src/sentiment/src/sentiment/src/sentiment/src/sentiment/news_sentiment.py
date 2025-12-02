# src/sentiment/news_sentiment.py
import requests
from textblob import TextBlob
import pandas as pd


# Example using NewsAPI (sign up needed) — but design function to accept an article list


def headlines_to_sentiment(headlines: list[str]):
scores = [TextBlob(h).sentiment.polarity for h in headlines]
if not scores:
return 0.0
return sum(scores) / len(scores)


# placeholder timeseries
def fetch_news_timeseries(start, end, force_refresh=False):
dates = pd.date_range(start, end, freq='D')
import numpy as np
arr = np.cumsum(np.random.randn(len(dates)))*0.01
return pd.DataFrame({"news_sentiment": arr}, index=dates)
