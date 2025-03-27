import time
from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.tasks import analyze_stock_task

# sudo docker exec -it stock_web python manage.py reanalyze_all
# For manually requesting a reanalyzing of all companies, Celery task scheduled for it


class Command(BaseCommand):
    help = "Re-analyze all companies in batches to prevent overload"

    def handle(self, *args, **options):
        symbols = list(Stock.objects.values_list("symbol", flat=True))
        total = len(symbols)
        batch_size = 5

        self.stdout.write(f"Starting re-analysis for {total} stocks in batches of {batch_size}...")

        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            for symbol in batch:
                analyze_stock_task.delay(symbol)
                self.stdout.write(f"Queued {symbol} for re-analysis")


            time.sleep(10)

        self.stdout.write(self.style.SUCCESS("All analysis tasks have been queued successfully."))
