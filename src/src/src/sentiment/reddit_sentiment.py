# src/sentiment/reddit_sentiment.py
import pandas as pd
from textblob import TextBlob
# using praw requires credentials; here we present a pluggable interface


def reddit_comments_to_sentiment(comments: list[str]):
# return simple polarity average
if not comments:
return 0.0
scores = [TextBlob(c).sentiment.polarity for c in comments]
return sum(scores) / len(scores)


# Example function that returns a daily time series (placeholder)
def fetch_reddit_timeseries(start, end, force_refresh=False):
dates = pd.date_range(start, end, freq='D')
# placeholder random walk
import numpy as np
arr = np.cumsum(np.random.randn(len(dates)))*0.01
return pd.DataFrame({"reddit_sentiment": arr}, index=dates)
