from rest_framework import serializers
from django.conf import settings
from ....models import Video

class VideoListSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'thumbnail',
            'genres',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'content',
            'created_at',
            'updated_at',
        ]

class VideoStreamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields =  [
            'id',
            'title',
            'description',
            'hls_path',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
    
    def to_representation(self, instance):
        val = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            val['hls_path'] = request.build_absolute_uri(f"/media/{instance.hls_path}")
        return val
