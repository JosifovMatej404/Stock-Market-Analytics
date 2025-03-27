from stocks.models import Stock, StockData, StockSignal
import pandas as pd
import numpy as np
from datetime import timedelta
from stocks.services.visualization import plot_candlestick_chart


def analyze_stock(symbol):
    try:
        stock = Stock.objects.get(symbol=symbol)
        data_qs = StockData.objects.filter(stock=stock).order_by('timestamp')

        if data_qs.count() < 20:  # Ensuring minimum data
            print(f"Not enough data to analyze {symbol}")
            return

        # Optimize DataFrame creation
        df = pd.DataFrame.from_records(data_qs.values('timestamp', 'open', 'high', 'low', 'close', 'volume'))
        df.set_index('timestamp', inplace=True)

        # Use NumPy for faster rolling calculations
        df['SMA_5'] = df['close'].rolling(window=5).mean().to_numpy()
        df['SMA_15'] = df['close'].rolling(window=15).mean().to_numpy()

        # Determine trend & action
        trend = "SIDEWAYS"
        action = "HOLD"
        if df['SMA_5'][-1] > df['SMA_15'][-1]:
            trend = "UP"
            action = "BUY"
        elif df['SMA_5'][-1] < df['SMA_15'][-1]:
            trend = "DOWN"
            action = "SELL"

        # Predict next day's close price (Linear Regression)
        df['timestamp_ordinal'] = df.index.map(pd.Timestamp.toordinal)
        x = df['timestamp_ordinal'].values[-15:].reshape(-1, 1)
        y = df['close'].values[-15:]

        coeffs = np.polyfit(x.flatten(), y, 1)
        next_day = df.index[-1] + timedelta(days=1)
        next_price = coeffs[0] * next_day.toordinal() + coeffs[1]

        # Generate visualization (ensures valid chart before saving)
        chart_html = plot_candlestick_chart(symbol)
        if not chart_html:
            print(f"No chart HTML generated for {symbol}, skipping save.")
            return

        # Save only if signal is meaningful
        StockSignal.objects.create(
            stock=stock,
            trend=trend,
            action=action,
            predicted_price=next_price,
            candle_chart_html=chart_html
        )

        print(f"✅ {symbol} analyzed → Trend: {trend} | Action: {action} | Predicted: ${next_price:.2f}")

    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
