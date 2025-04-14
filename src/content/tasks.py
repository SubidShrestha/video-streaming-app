import os
import subprocess
from celery import shared_task
from django.conf import settings
from .models import Video

@shared_task
def convert_video_to_hls(video_id):
    try:
        video = Video.objects.get(id=video_id)
        input_path = video.content.path
        output_dir = os.path.join(settings.MEDIA_ROOT, f'hls/{video_id}')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'index.m3u8')

        command = [
            'ffmpeg', '-i', input_path,
            '-profile:v', 'baseline', '-level', '3.0',
            '-start_number', '0', '-hls_time', '10',
            '-hls_list_size', '0', '-f', 'hls',
            output_path,
        ]
        subprocess.run(command, check=True)

        video.hls_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
        video.is_processing = False
        video.save(update_fields=['hls_path', 'is_processing'])

    except subprocess.CalledProcessError as e:
        print(f"[FFmpeg Error] {e}")
    except Exception as e:
        print(f"[Unhandled Error] {e}")