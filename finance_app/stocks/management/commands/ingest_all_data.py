from django.core.management.base import BaseCommand
from stocks.tasks import batch_ingest_all_symbols

# sudo docker compose exec web python manage.py ingest_all_data
# Calls neccessery functionalities to collect and store data for all companies in the database

class Command(BaseCommand):
    help = "Triggers historical ingestion for all S&P 500 stocks (via Celery)"

    def handle(self, *args, **kwargs):
        batch_ingest_all_symbols.delay()
        self.stdout.write(self.style.SUCCESS("✅ Queued all historical ingestion tasks."))
