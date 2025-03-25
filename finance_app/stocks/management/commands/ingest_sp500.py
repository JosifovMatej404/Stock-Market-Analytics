from django.core.management.base import BaseCommand
from stocks.services.ingestion import store_sp500_symbols

class Command(BaseCommand):
    help = "Ingests current S&P 500 stock symbols into the database"

    def handle(self, *args, **kwargs):
        store_sp500_symbols()
