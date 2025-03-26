# stocks/services/ingestion.py

import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime
from stocks.models import Stock, StockData

def fetch_historical_data(symbol: str, period="5y", interval="1d"):
    print(f"Fetching historical data for {symbol} ({period}, {interval})")

    df = yf.download(symbol, period=period, interval=interval, progress=False)

    if df.empty:
        print(f" No data returned for {symbol}")
        return

    # Flatten MultiIndex if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    stock, _ = Stock.objects.get_or_create(symbol=symbol)

    for timestamp, row in df.iterrows():
        dt = timestamp.to_pydatetime().replace(tzinfo=pytz.UTC)

        try:
            StockData.objects.update_or_create(
                stock=stock,
                timestamp=dt,
                defaults={
                    'open': float(row['Open']) if pd.notna(row['Open']) else 0.0,
                    'high': float(row['High']) if pd.notna(row['High']) else 0.0,
                    'low': float(row['Low']) if pd.notna(row['Low']) else 0.0,
                    'close': float(row['Close']) if pd.notna(row['Close']) else 0.0,
                    'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0
                }
            )
        except Exception as e:
            print(f"Skipping row at {dt} due to error: {e}")
            continue

    print(f"Done: {symbol}")


def get_sp500_symbols():
    """
    Scrapes current S&P 500 symbols from Wikipedia.
    Returns a list of ticker symbols (Yahoo Finance compatible).
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]

    # Clean symbols: replace "." with "-" for Yahoo Finance
    symbols = df['Symbol'].str.replace('.', '-', regex=False).tolist()

    return symbols



def store_sp500_symbols():
    """
    Stores S&P 500 tickers in the database (Stock model).
    """
    symbols = get_sp500_symbols()
    for symbol in symbols:
        Stock.objects.get_or_create(symbol=symbol)
    print(f"✅ Stored {len(symbols)} S&P 500 symbols.")


def fetch_all_realtime_data():
    """
    Fetches the latest 1-minute data for all tracked stocks in DB.
    """
    print("Starting realtime batch fetch...")
    stocks = Stock.objects.all()

    for stock in stocks:
        try:
            ticker = yf.Ticker(stock.symbol)
            df = ticker.history(period="1d", interval="1m", prepost=False)

            if df.empty:
                print(f"No data for {stock.symbol}")
                continue

            latest_timestamp = df.index[-1].to_pydatetime().replace(tzinfo=pytz.UTC)
            latest_row = df.iloc[-1]

            StockData.objects.update_or_create(
                stock=stock,
                timestamp=latest_timestamp,
                defaults={
                    "open": float(latest_row["Open"]),
                    "high": float(latest_row["High"]),
                    "low": float(latest_row["Low"]),
                    "close": float(latest_row["Close"]),
                    "volume": int(latest_row["Volume"]),
                }
            )

            print(f" {stock.symbol} stored at {latest_timestamp}")

        except Exception as e:
            print(f" Error for {stock.symbol}: {e}")

    print("Realtime batch fetch complete.")
