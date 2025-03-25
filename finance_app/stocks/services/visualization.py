import pandas as pd
from stocks.models import Stock, StockData
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime, timedelta


def plot_candlestick_chart(symbol, days=90):
    stock = Stock.objects.get(symbol=symbol)

    # Get only the most recent `days` worth of data
    cutoff = datetime.now() - timedelta(days=days)
    data_qs = StockData.objects.filter(stock=stock, timestamp__gte=cutoff).order_by('timestamp')

    if not data_qs.exists():
        return None

    df = pd.DataFrame.from_records(data_qs.values('timestamp', 'open', 'high', 'low', 'close'))
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=symbol
    )])

    fig.update_layout(
        title=f"{symbol} - Candlestick Chart (Last {days} Days)",
        xaxis_rangeslider_visible=True,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        margin=dict(l=30, r=30, t=40, b=30),
    )

    return plot(fig, output_type='div')
