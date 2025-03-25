from django.core.management.base import BaseCommand
from stocks.tasks import batch_ingest_all_symbols

class Command(BaseCommand):
    help = "Triggers historical ingestion for all S&P 500 stocks (via Celery)"

    def handle(self, *args, **kwargs):
        batch_ingest_all_symbols.delay()
        self.stdout.write(self.style.SUCCESS("✅ Queued all historical ingestion tasks."))
