from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.tasks import analyze_stock_task
import time
from celery.result import AsyncResult

class Command(BaseCommand):
    help = "Re-analyze all companies and regenerate signals + chart HTML"

    def handle(self, *args, **options):
        symbols = list(Stock.objects.values_list("symbol", flat=True))
        total = len(symbols)

        if not symbols:
            self.stdout.write(self.style.ERROR("No stocks found in the database!"))
            return

        self.stdout.write(self.style.WARNING(f"🔥 Starting re-analysis for {total} stocks..."))

        
        MAX_CONCURRENT = 3
        running_tasks = {}

        idx = 0
        while idx < len(symbols) or running_tasks:

            finished_tasks = [
                task_id for task_id, async_result in running_tasks.items()
                if async_result.ready()
            ]
            for task_id in finished_tasks:
                running_tasks.pop(task_id)
                self.stdout.write(self.style.SUCCESS(f"✅ Completed: {task_id}"))


            while len(running_tasks) < MAX_CONCURRENT and idx < len(symbols):
                symbol = symbols[idx]
                async_result = analyze_stock_task.delay(symbol)
                running_tasks[symbol] = async_result
                self.stdout.write(f"🚀 [{idx+1}/{total}] Queued analysis for {symbol}")
                idx += 1


            time.sleep(10)

        self.stdout.write(self.style.SUCCESS("🎉All analysis tasks completed successfully!"))
