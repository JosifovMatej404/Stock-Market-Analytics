from django.core.management.base import BaseCommand
from stocks.services.ingestion import store_sp500_symbols

# sudo docker compose exec web python manage.py ingest_sp500
# Calls the functions to collect all of the S&P 500 company symbols (TICKERS)


class Command(BaseCommand):
    help = "Ingests current S&P 500 stock symbols into the database"

    def handle(self, *args, **kwargs):
        store_sp500_symbols()
