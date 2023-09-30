from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PulsePoint.settings")
app = Celery("PulsePoint")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "send_daily_quote": {
        "task": "yourapp.management.commands.send_daily_quote",
        "schedule": crontab(hour=0, minute=5),
        },
}

app.autodiscover_tasks()