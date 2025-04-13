import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_streaming.settings')

app = Celery('video_streaming')

app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()