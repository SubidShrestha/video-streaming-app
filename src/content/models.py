from django.db import models
from django.utils.translation import gettext_lazy as _
from shared.mixins.model_mixins import AbstractTimestampMixin, AbstractStatusMixin, AbstractUserstampMixin

class Genre(AbstractTimestampMixin):
    name = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=24, unique=True)

    class Meta:
        db_table = 'genres'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
    
    def __str__(self) -> str:
        return f"Genre <{self.name}>"

class Video(AbstractTimestampMixin, AbstractStatusMixin, AbstractUserstampMixin):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    thumbnail = models.ImageField(upload_to='video/thumbnails/')
    content = models.FileField(upload_to='video/contents/')
    hls_path = models.CharField(max_length=512, blank=True, null=True)
    is_processing = models.BooleanField(default=True)
    genres = models.ManyToManyField(Genre, related_name='videos', through='VideoGenre')

    class Meta:
        db_table = 'videos'
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
    
    def __str__(self) -> str:
        return f"Video <{self.title}>"

class VideoGenre(AbstractTimestampMixin):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'video_genres'
        verbose_name = _('Video Genre')
        verbose_name_plural = _('Video Genres')
        unique_together = (('video', 'genre',),)
    
    def __str__(self) -> str:
        return f"Video <{self.video}> - Genre <{self.genre}>"
