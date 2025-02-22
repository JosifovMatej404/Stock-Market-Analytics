import yfinance as yf
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

# Function to fetch real-time stock data
def get_realtime_data(ticker='ADBE'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1d', interval='5m')  # Fetch last day, 5-min intervals
    df = hist[['Open', 'High', 'Low', 'Close']].reset_index()
    df['Datetime'] = df['Datetime'].dt.strftime('%Y-%m-%d %H:%M')
    return df

# Dash App Setup
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Real-Time ADBE Stock Candlestick Chart"),
    dcc.Graph(id='candlestick-chart'),
    dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0)  # Update every 10 seconds
])

@app.callback(Output('candlestick-chart', 'figure'), Input('interval-component', 'n_intervals'))
def update_chart(_):
    candlestick_df = get_realtime_data()
    fig = go.Figure(data=[go.Candlestick(
        x=candlestick_df['Datetime'],
        open=candlestick_df['Open'],
        high=candlestick_df['High'],
        low=candlestick_df['Low'],
        close=candlestick_df['Close']
    )])
    fig.update_layout(title='Adobe Inc. (ADBE) Real-Time Candlestick Chart', xaxis_title='Time', yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)  # Runs the Dash web server
