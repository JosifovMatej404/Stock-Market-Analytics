from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.tasks import analyze_stock_task
from celery import group
import time
import random

class Command(BaseCommand):
    help = "Re-analyze all companies and regenerate signals + chart HTML in batches"

    def handle(self, *args, **options):
        symbols = list(Stock.objects.values_list("symbol", flat=True))

        if not symbols:
            self.stdout.write(self.style.ERROR("❌ No stocks found in the database!"))
            return

        batch_size = 10  # 🔥 Adjust batch size based on available resources
        total_batches = (len(symbols) // batch_size) + 1

        self.stdout.write(self.style.SUCCESS(f"🚀 Starting reanalysis for {len(symbols)} stocks..."))

        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            self.stdout.write(f"📊 Processing batch {i // batch_size + 1} of {total_batches}...")

            # 🔥 Launch batch Celery tasks
            job_group = group(analyze_stock_task.s(symbol) for symbol in batch)
            result = job_group.apply_async()

            # 🔥 Wait for the batch to complete before moving to the next one
            while not result.ready():
                self.stdout.write("⏳ Waiting for batch to complete...")
                time.sleep(random.randint(30, 60))  # Wait 30-60 seconds before the next batch

        self.stdout.write(self.style.SUCCESS("🎉 Reanalysis completed successfully!"))
