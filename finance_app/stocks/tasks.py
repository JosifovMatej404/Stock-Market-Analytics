# stocks/tasks.py
# stocks/tasks.py

from celery import shared_task
from stocks.services.ingestion import fetch_historical_data
from stocks.models import Stock

@shared_task
def ingest_historical_task(symbol):
    """
    Celery task to run historical ingestion for a given stock symbol.
    """
    fetch_historical_data(symbol)
    return f"Historical data fetched for {symbol}"


@shared_task
def batch_ingest_all_symbols():
    """
    Celery task to trigger historical ingestion for all S&P 500 stocks.
    """
    symbols = Stock.objects.values_list("symbol", flat=True)
    for symbol in symbols:
        ingest_historical_task.delay(symbol)
    return f"✅ Queued {len(symbols)} ingestion tasks."