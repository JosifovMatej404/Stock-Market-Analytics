import time
from django.core.management.base import BaseCommand
from celery.result import AsyncResult
from stocks.models import Stock
from stocks.tasks import analyze_stock_task

class Command(BaseCommand):
    help = "Re-analyze all stocks and generate new signals + chart HTML."

    def handle(self, *args, **options):
        symbols = list(Stock.objects.values_list("symbol", flat=True))
        total = len(symbols)

        if not symbols:
            self.stdout.write(self.style.ERROR("❌ No stocks found!"))
            return

        self.stdout.write(f"🔥 Starting re-analysis for {total} stocks...")

        active_tasks = []
        max_concurrent_tasks = 3 

        for idx, symbol in enumerate(symbols, start=1):
            # Wait if active tasks are at max limit
            while len(active_tasks) >= max_concurrent_tasks:
                time.sleep(2)
                active_tasks = [task for task in active_tasks if not AsyncResult(task.id).ready()]

            # Queue new task
            task = analyze_stock_task.delay(symbol)
            active_tasks.append(task)

            self.stdout.write(f"🚀 [{idx}/{total}] Queued analysis for {symbol}")

            # Reduce CPU spike by adding a delay
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("✅ All analysis tasks have been queued!"))
