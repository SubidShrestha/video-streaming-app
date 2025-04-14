from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import permissions
from ....models import Video
from ..serializers.video import VideoListSerializer, VideoCreateSerializer, VideoStreamingSerializer
from ....tasks import convert_video_to_hls

@method_decorator(
    decorator=extend_schema(
        tags=['Video(s)'],
        operation_id='list-videos',
        summary='API to list the videos along with their thumbnails',
    ),
    name='get'
)
@method_decorator(
    decorator=extend_schema(
        tags=['Video(s)'],
        operation_id='create-videos',
        summary='API to create videos',
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class VideoView(generics.ListCreateAPIView):
    """API to list all the videos"""
    queryset = Video.objects.prefetch_related('genres').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VideoListSerializer
        elif self.request.method == 'POST':
            return VideoCreateSerializer
        else:
            raise exceptions.ParseError(_('Corrupted Request'))
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
        convert_video_to_hls.delay(serializer.instance.pk)

@method_decorator(
    decorator=extend_schema(
        tags=['Video(s)'],
        operation_id='stream-videos',
        summary='API to watch videos',
    ),
    name='get'
)
class VideoStreamView(generics.RetrieveAPIView):
    """API to stream videos"""
    serializer_class = VideoStreamingSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.prefetch_related('genres').all()
