import dash
from dash import dcc, html
import plotly.graph_objs as go
import requests
import time

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Live AAPL Stock Prices"),
    dcc.Graph(id="live-stock-chart"),
    dcc.Interval(
        id="interval-component",
        interval=5000,  # Update every 5 seconds
        n_intervals=0
    )
])

def fetch_data():
    try:
        response = requests.get("http://localhost:5000/stocks")
        return response.json()
    except:
        return []

@app.callback(
    dash.Output("live-stock-chart", "figure"),
    [dash.Input("interval-component", "n_intervals")]
)
def update_chart(n):
    data = fetch_data()
    if not data:
        return go.Figure()

    timestamps = [d["timestamp"] for d in data]
    prices = [d["close"] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=prices, mode="lines+markers", name="AAPL"))

    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
