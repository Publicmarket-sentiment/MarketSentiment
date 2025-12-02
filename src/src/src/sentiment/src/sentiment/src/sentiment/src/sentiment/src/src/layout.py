# src/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc


def build_layout():
layout = html.Div([
html.H2("US Market Sentiment Dashboard"),
html.Div([
dcc.DatePickerRange(id='date-range', start_date_placeholder_text='Start', end_date_placeholder_text='End'),
html.Button('Refresh', id='refresh-button'),
dcc.Checklist(id='auto-refresh-toggle', options=[{"label":"Auto-refresh","value":"on"}], value=[]),
dcc.Interval(id='refresh-interval', interval=60*1000, disabled=True)
]),
dcc.Graph(id='spy-chart'),
dcc.Graph(id='vix-chart'),
dcc.Graph(id='putcall-chart'),
dcc.Graph(id='short-interest-chart'),
dcc.Graph(id='reddit-sentiment-chart'),
dcc.Graph(id='twitter-sentiment-chart'),
dcc.Graph(id='trends-chart'),
dcc.Graph(id='news-sentiment-chart'),
html.Div(id='fear-greed-display')
])
return layout
