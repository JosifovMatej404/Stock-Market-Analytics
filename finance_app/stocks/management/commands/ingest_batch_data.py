from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.tasks import ingest_historical_task
import time


class Command(BaseCommand):
    help = "Ingests stock data in batches to avoid overloading the system."

    def handle(self, *args, **kwargs):
        batch_size = 25  # Adjust based on performance
        stocks = list(Stock.objects.all())

        self.stdout.write(self.style.SUCCESS(f"📊 Found {len(stocks)} stocks. Starting batch ingestion..."))

        for i in range(0, len(stocks), batch_size):
            batch = stocks[i:i + batch_size]
            self.stdout.write(
                self.style.WARNING(f"🚀 Processing batch {i // batch_size + 1}/{(len(stocks) // batch_size) + 1}..."))

            for stock in batch:
                ingest_historical_task.delay(stock.symbol)  # Celery task for ingestion
                time.sleep(1)  # Small delay to avoid API rate limits

            self.stdout.write(self.style.SUCCESS("✅ Batch completed! Waiting before next batch..."))
            time.sleep(5)  # Prevent overloading APIs

        self.stdout.write(self.style.SUCCESS("🎉 All stock data ingested successfully!"))
