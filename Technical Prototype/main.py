import yfinance as yf
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(url)
df = table[0]  # First table contains S&P 500 companies

# Get tickers and issuers
tickers = df["Symbol"].tolist()
issuers = df["Security"].tolist()

data = yf.download(tickers=tickers[5], period="1000d")
print(data)
print("--------------")
print(data.values)
print("--------------")
print(data.keys())


# Sample data in MultiIndex format
index = pd.MultiIndex.from_tuples([
    ('Close', tickers[5]), ('High', tickers[5]), ('Low', tickers[5]), ('Open', tickers[5]), ('Volume', tickers[5])],
    names=['Price', 'Ticker']
)
values = data.values
df = pd.DataFrame(values, columns=index)

# Convert MultiIndex DataFrame to standard format
candlestick_df = pd.DataFrame({
    'Date': pd.date_range(start='2024-02-01', periods=len(df), freq='D'),
    'Open': df[('Open', tickers[5])],
    'High': df[('High', tickers[5])],
    'Low': df[('Low', tickers[5])],
    'Close': df[('Close', tickers[5])]
})

# Dash App Setup
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1(tickers[5] + " Stock Candlestick Chart"),
    dcc.Graph(id='candlestick-chart')
])

@app.callback(Output('candlestick-chart', 'figure'), Input('candlestick-chart', 'id'))
def update_chart(_):
    fig = go.Figure(data=[go.Candlestick(
        x=candlestick_df['Date'],
        open=candlestick_df['Open'],
        high=candlestick_df['High'],
        low=candlestick_df['Low'],
        close=candlestick_df['Close']
    )])
    fig.update_layout(title='Adobe Inc. (ADBE) Candlestick Chart', xaxis_title='Date', yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)  # Runs the Dash web server