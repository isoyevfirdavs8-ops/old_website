import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dunyo_textile.settings")

app = Celery("dunyo_textile")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()