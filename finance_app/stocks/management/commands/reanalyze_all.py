from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.tasks import analyze_stock_task
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class Command(BaseCommand):
    help = "Re-analyze all companies and regenerate signals + chart HTML with 3 concurrent tasks"

    def handle(self, *args, **options):
        symbols = list(Stock.objects.values_list("symbol", flat=True))
        total = len(symbols)

        self.stdout.write(f"🔥 Starting re-analysis for {total} stocks...")

        # Max 3 tasks running at once
        max_concurrent_tasks = 3
        completed = 0

        with ThreadPoolExecutor(max_workers=max_concurrent_tasks) as executor:
            future_to_symbol = {}

            # Start first batch of 3
            for _ in range(min(max_concurrent_tasks, len(symbols))):
                symbol = symbols.pop(0)
                future = executor.submit(analyze_stock_task.delay, symbol)
                future_to_symbol[future] = symbol
                self.stdout.write(f"🚀 Queued analysis for {symbol}")

            # Process remaining tasks as others finish
            while future_to_symbol:
                for future in as_completed(future_to_symbol):
                    symbol = future_to_symbol.pop(future)
                    completed += 1
                    self.stdout.write(f"✅ Completed: {symbol} ({completed}/{total})")

                    if symbols:
                        next_symbol = symbols.pop(0)
                        next_future = executor.submit(analyze_stock_task.delay, next_symbol)
                        future_to_symbol[next_future] = next_symbol
                        self.stdout.write(f"🚀 Queued analysis for {next_symbol}")

                    # Small delay to prevent overload
                    time.sleep(1)

        self.stdout.write(self.style.SUCCESS("🎉 All stocks analyzed successfully!"))
