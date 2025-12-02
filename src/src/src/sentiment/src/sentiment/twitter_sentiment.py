# src/sentiment/twitter_sentiment.py
# Use snscrape (no credentials) to fetch tweets or tweepy for API-based approach.
# Here we supply a pluggable function signature and a simple example.
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def text_sentiment_vader(text: str):
return analyzer.polarity_scores(text)["compound"]


def fetch_twitter_timeseries(start, end, query="#SPY OR $SPY", max_tweets=500, force_refresh=False):
dates = pd.date_range(start, end, freq='D')
import numpy as np
arr = np.cumsum(np.random.randn(len(dates)))*0.01
return pd.DataFrame({"twitter_sentiment": arr}, index=dates)
