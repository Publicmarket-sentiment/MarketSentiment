import dash
from dash import html, dcc
import plotly.graph_objs as go
import base64
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from data.market_data import get_spy, get_vix, get_put_call_ratio
from data.reddit_sentiment import fetch_reddit_sentiment
from data.news_sentiment import fetch_news_sentiment
from data.google_trends import fetch_trends
from ml.next_day_prediction import get_next_day_prediction

# Dash app
app = dash.Dash(__name__)
server = app.server

# Convert figures to images
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")

app.layout = html.Div([
    html.H1("📈 US Stock Market Sentiment Dashboard", style={"textAlign": "center"}),

    dcc.Interval(id="refresh", interval=60000, n_intervals=0),

    html.Div([
        html.Div(id="spy-chart", style={"width": "48%", "display": "inline-block"}),
        html.Div(id="vix-chart", style={"width": "48%", "display": "inline-block"}),
    ]),

    html.Div([
        html.Div(id="pcr-box", style={"width": "32%", "display": "inline-block"}),
        html.Div(id="reddit-sent", style={"width": "32%", "display": "inline-block"}),
        html.Div(id="news-sent", style={"width": "32%", "display": "inline-block"}),
    ]),

    html.Div([
        html.Div(id="trends-chart", style={"width": "48%", "display": "inline-block"}),
        html.Div(id="ml-prediction", style={"width": "48%", "display": "inline-block"}),
    ]),

    html.Div([
        html.Div(id="wordcloud", style={"width": "100%"})
    ]),
])

@app.callback(
    [
        dash.Output("spy-chart", "children"),
        dash.Output("vix-chart", "children"),
        dash.Output("pcr-box", "children"),
        dash.Output("reddit-sent", "children"),
        dash.Output("news-sent", "children"),
        dash.Output("trends-chart", "children"),
        dash.Output("ml-prediction", "children"),
        dash.Output("wordcloud", "children"),
    ],
    [dash.Input("refresh", "n_intervals")]
)
def update_dashboard(n):
    spy = get_spy()
    vix = get_vix()

    fig_spy = go.Figure(data=[go.Scatter(x=spy.index, y=spy.Close)])
    fig_spy.update_layout(title="SPY", template="plotly_dark")

    fig_vix = go.Figure(data=[go.Scatter(x=vix.index, y=vix.Close)])
    fig_vix.update_layout(title="VIX", template="plotly_dark")

    pcr = get_put_call_ratio()

    reddit_df = fetch_reddit_sentiment()
    reddit_fig = go.Figure(data=[go.Bar(x=reddit_df["post"], y=reddit_df["sentiment"])])
    reddit_fig.update_layout(template="plotly_dark", title="Reddit WSB Sentiment")

    news_df = fetch_news_sentiment()
    news_fig = go.Figure(data=[go.Bar(x=news_df["title"], y=news_df["sentiment"])])
    news_fig.update_layout(template="plotly_dark", title="News Sentiment")

    trend_df = fetch_trends()
    trends_fig = go.Figure(data=[go.Scatter(x=trend_df.index, y=trend_df["SPY"])])
    trends_fig.update_layout(template="plotly_dark", title="Google Trends: SPY")

    signal, value = get_next_day_prediction()

    text = " ".join(reddit_df["post"])
    wc = WordCloud(background_color="black", colormap="viridis").generate(text)
    fig_wc = plt.figure(figsize=(10, 4))
    plt.imshow(wc)
    plt.axis("off")
    wc_img = fig_to_base64(fig_wc)

    return (
        dcc.Graph(figure=fig_spy),
        dcc.Graph(figure=fig_vix),
        html.H3(f"Put/Call Ratio: {pcr}"),
        dcc.Graph(figure=reddit_fig),
        dcc.Graph(figure=news_fig),
        dcc.Graph(figure=trends_fig),
        html.H2(f"Next-Day Prediction: {signal} ({value:.4f})"),
        html.Img(src="data:image/png;base64," + wc_img),
    )

if __name__ == "__main__":
    app.run_server(debug=True)
