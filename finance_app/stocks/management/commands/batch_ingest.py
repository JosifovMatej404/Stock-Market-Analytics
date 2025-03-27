import time
import random
from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.services.ingestion import fetch_historical_data  # Ensure this exists

class Command(BaseCommand):
    help = "Batch ingestion of historical stock data"

    def handle(self, *args, **kwargs):
        stocks = list(Stock.objects.values_list('symbol', flat=True))

        if not stocks:
            self.stdout.write(self.style.ERROR("❌ No stocks found in database!"))
            return

        batch_size = 25
        total_batches = (len(stocks) // batch_size) + 1

        self.stdout.write(self.style.SUCCESS(f"🔥 Starting batch ingestion for {len(stocks)} stocks..."))

        for i in range(0, len(stocks), batch_size):
            batch = stocks[i:i + batch_size]
            self.stdout.write(self.style.WARNING(f"📦 Processing batch {i // batch_size + 1} of {total_batches}..."))

            for symbol in batch:
                try:
                    fetch_historical_data(symbol)  # Correct function call
                    self.stdout.write(self.style.SUCCESS(f"✅ Ingested {symbol}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Error processing {symbol}: {e}"))

            # Avoid hitting API limits → wait 60-90 sec between batches
            wait_time = random.randint(60, 90)
            self.stdout.write(self.style.WARNING(f"⏳ Waiting {wait_time}s before next batch..."))
            time.sleep(wait_time)

        self.stdout.write(self.style.SUCCESS("🎉 Batch ingestion completed!"))
