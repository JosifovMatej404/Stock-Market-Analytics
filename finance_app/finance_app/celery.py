# finance_app/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_app.settings')

app = Celery('finance_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_soft_time_limit = 60  
app.conf.worker_prefetch_multiplier = 1