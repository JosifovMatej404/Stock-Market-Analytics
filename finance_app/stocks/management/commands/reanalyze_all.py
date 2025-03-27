import time
from stocks.models import Stock
from stocks.services.analysis import analyze_stock

class Command(BaseCommand):
    help = "Re-analyze all companies one-by-one, ensuring completion before moving to next"

    def handle(self, *args, **options):
        symbols = list(Stock.objects.values_list("symbol", flat=True))
        total = len(symbols)

        if not symbols:
            self.stdout.write(self.style.WARNING("No stocks found in database!"))
            return

        self.stdout.write(f" Starting sequential re-analysis for {total} stocks...")

        for idx, symbol in enumerate(symbols, start=1):
            success = False
            retries = 3  # Retries per stock in case of failure

            for attempt in range(retries):
                try:
                    self.stdout.write(f"🔍 [{idx}/{total}] Analyzing {symbol}... (Attempt {attempt + 1})")
                    analyze_stock(symbol)
                    self.stdout.write(self.style.SUCCESS(f"✅ {symbol} analysis completed!"))
                    success = True
                    break  # Move to next stock if successful
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error analyzing {symbol}: {e}"))

            if not success:
                self.stdout.write(self.style.ERROR(f" {symbol} failed after {retries} attempts, skipping!"))

            # Small delay to prevent overloading CPU/DB
            time.sleep(2)  # Adjust if needed

        self.stdout.write(self.style.SUCCESS(" Re-analysis process completed!"))
