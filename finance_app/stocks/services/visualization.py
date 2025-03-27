import pandas as pd
from stocks.models import Stock, StockData
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime, timedelta

def plot_candlestick_chart(symbol, days=366):
    stock = Stock.objects.get(symbol=symbol)

    # Optimize query by selecting only required fields
    cutoff = datetime.now() - timedelta(days=days)
    data_qs = StockData.objects.filter(stock=stock, timestamp__gte=cutoff).order_by('timestamp')

    if not data_qs.exists():
        return None


    df = pd.DataFrame.from_records(data_qs.values('timestamp', 'open', 'high', 'low', 'close'))
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Construct figure
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=symbol
    ))

    # Optimize layout rendering
    fig.update_layout(
        title=f"{symbol} - Candlestick Chart ({days} Days)",
        xaxis_rangeslider_visible=False,  # Removes unnecessary slider
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        margin=dict(l=20, r=20, t=30, b=20),  # Less padding for better fit
    )

    return plot(fig, output_type='div')
