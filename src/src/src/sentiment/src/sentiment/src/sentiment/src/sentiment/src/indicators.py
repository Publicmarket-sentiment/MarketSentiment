# src/indicators.py
import pandas as pd


def rolling_zscore(series: pd.Series, window=30):
return (series - series.rolling(window).mean()) / series.rolling(window).std()


def fear_and_greed_index(components: dict):
# components: {name: pd.Series aligned on index}
df = pd.DataFrame(components)
z = df.apply(lambda s: (s - s.mean()) / s.std(), axis=0)
# weight equally then scale 0-100
combined = z.mean(axis=1)
scaled = 50 + (combined - combined.min()) / (combined.max() - combined.min()) * 50
return scaled.clip(0,100)
