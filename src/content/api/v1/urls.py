from django.urls import path
from .views.video import VideoView, VideoStreamView

urlpatterns = [
    path('video/', VideoView.as_view(), name='video'),
    path('stream/<int:pk>', VideoStreamView.as_view(), name='stream'),
]
