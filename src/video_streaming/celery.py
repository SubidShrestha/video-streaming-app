import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_streaming.settings')

app = Celery('video_streaming')

app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks(
    [
        'authentication.tasks.send_register_mail',
        'authentication.tasks.send_reset_mail',
        'content.tasks.convert_video_to_hls',
    ]
)