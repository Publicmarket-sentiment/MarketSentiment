# src/callbacks.py
from dash import Input, Output, State
from dash import callback
from datetime import datetime, timedelta
from .data_fetch import fetch_spy, fetch_vix
from .sentiment.reddit_sentiment import fetch_reddit_timeseries
from .sentiment.twitter_sentiment import fetch_twitter_timeseries
from .indicators import fear_and_greed_index
import pandas as pd


# enable/disable interval from checklist
@callback(Output('refresh-interval', 'disabled'), Input('auto-refresh-toggle', 'value'))
def toggle_interval(vals):
return (len(vals) == 0)


# master refresh callback triggered by button or interval
@callback(
Output('spy-chart', 'figure'),
Output('vix-chart', 'figure'),
Output('fear-greed-display', 'children'),
Input('refresh-button', 'n_clicks'),
Input('refresh-interval', 'n_intervals'),
State('date-range', 'start_date'),
State('date-range', 'end_date')
)
def refresh_all(n_clicks, n_intervals, start, end):
# default date range
if start is None or end is None:
end = datetime.today().date()
start = end - timedelta(days=365)
spy = fetch_spy(start=start, end=end)
vix = fetch_vix(start=start, end=end)
reddit = fetch_reddit_t
