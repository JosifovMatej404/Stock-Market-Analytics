from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks.services.analysis import analyze_stock  # Directly import the function


class Command(BaseCommand):
    help = "Re-analyze all stocks one by one (without Celery or threads)."

    def handle(self, *args, **options):
        symbols = Stock.objects.values_list("symbol", flat=True)
        total = len(symbols)

        self.stdout.write(self.style.WARNING(f"🔥 Starting sequential re-analysis for {total} stocks..."))

        for idx, symbol in enumerate(symbols, start=1):
            self.stdout.write(f"🔍 [{idx}/{total}] Analyzing {symbol}...")

            try:
                analyze_stock(symbol)  # Direct function call
                self.stdout.write(self.style.SUCCESS(f"✅ Completed: {symbol}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error analyzing {symbol}: {e}"))

        self.stdout.write(self.style.SUCCESS("🎉 All stocks analyzed successfully!"))
