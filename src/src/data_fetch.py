# src/data_fetch.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .cache import cached


@cached("spy_vix", expire_seconds=60*5)
def fetch_spy(start: str, end: str, force_refresh=False):
ticker = yf.Ticker("SPY")
df = ticker.history(start=start, end=end, interval="1d")[['Close','Volume']]
df = df.rename(columns={'Close':'spy_close'})
return df


@cached("vix", expire_seconds=60*10)
def fetch_vix(start: str, end: str, force_refresh=False):
vix = yf.Ticker("^VIX")
df = vix.history(start=start, end=end, interval="1d")[['Close']]
df = df.rename(columns={'Close':'vix_close'})
return df


# placeholder: put/call ratio and short interest often come from vendor APIs — provide a function that accepts a fallback CSV
def load_put_call(filepath=None):
if filepath:
return pd.read_csv(filepath, parse_dates=["date"]).set_index("date")
# else: return example synthetic series
dates = pd.date_range(datetime.today() - timedelta(days=365), periods=365)
return pd.DataFrame({"put_call": 0.6 + 0.1 * (pd.np.sin(range(365))/1)}, index=dates)


# short interest: same approach — vendor API recommended
