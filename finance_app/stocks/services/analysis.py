from stocks.models import Stock, StockData, StockSignal
import pandas as pd
from datetime import timedelta
import numpy as np
from stocks.services.visualization import plot_candlestick_chart  # <- Important!

def analyze_stock(symbol):
    try:
        stock = Stock.objects.get(symbol=symbol)
        data_qs = StockData.objects.filter(stock=stock).order_by('timestamp')
        if data_qs.count() < 20:
            print(f"Not enough data to analyze {symbol}")
            return

        df = pd.DataFrame.from_records(
            data_qs.values('timestamp', 'open', 'high', 'low', 'close', 'volume')
        )
        df.set_index('timestamp', inplace=True)

        # Calculate moving averages
        df['SMA_5'] = df['close'].rolling(window=5).mean()
        df['SMA_15'] = df['close'].rolling(window=15).mean()

        # Detect trend
        if df['SMA_5'].iloc[-1] > df['SMA_15'].iloc[-1]:
            trend = "UP"
        elif df['SMA_5'].iloc[-1] < df['SMA_15'].iloc[-1]:
            trend = "DOWN"
        else:
            trend = "SIDEWAYS"

        # Simple action suggestion
        action = {"UP": "BUY", "DOWN": "SELL", "SIDEWAYS": "HOLD"}[trend]

        # Predict next close using linear regression
        df['timestamp_ordinal'] = df.index.map(pd.Timestamp.toordinal)
        x = df['timestamp_ordinal'].values[-15:].reshape(-1, 1)
        y = df['close'].values[-15:]
        coeffs = np.polyfit(x.flatten(), y, 1)
        next_day = df.index[-1] + timedelta(days=1)
        next_price = coeffs[0] * next_day.toordinal() + coeffs[1]

        # Generate candlestick HTML
        chart_html = plot_candlestick_chart(symbol)
        if not chart_html:
            print(f"No chart HTML for {symbol}")
            return

        StockSignal.objects.create(
            stock=stock,
            trend=trend,
            action=action,
            predicted_price=next_price,
            candle_chart_html=chart_html
        )
        print(f"{symbol} analyzed → {trend} | {action} | Predicted ${next_price:.2f}")

    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
