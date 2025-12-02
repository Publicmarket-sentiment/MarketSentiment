# src/sentiment/google_trends.py
from pytrends.request import TrendReq
import pandas as pd


pytrends = TrendReq(hl='en-US', tz=360)


def fetch_trends_timeseries(keyword: str, start_date: str, end_date: str, force_refresh=False):
timeframe = f"{start_date} {end_date}"
pytrends.build_payload([keyword], timeframe=timeframe)
data = pytrends.interest_over_time()
if data.empty:
return pd.DataFrame()
data = data.drop(columns=['isPartial'], errors='ignore')
return data
