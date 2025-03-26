from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.tasks import analyze_stock_task

class Command(BaseCommand):
    help = "Re-analyze all companies and regenerate signals + chart HTML"

    def handle(self, *args, **options):
        symbols = Stock.objects.values_list("symbol", flat=True)
        total = len(symbols)

        for idx, symbol in enumerate(symbols, start=1):
            analyze_stock_task.delay(symbol)
            self.stdout.write(f"[{idx}/{total}] Queued re-analysis for {symbol}")

        self.stdout.write(self.style.SUCCESS("All analysis tasks have been queued successfully."))
