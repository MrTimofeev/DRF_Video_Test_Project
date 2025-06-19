from rest_framework import serializers
from videos.models import Video, Like, VideoFile


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['video', 'user']
        read_only_fields = ['user']


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ['id', 'file', 'quantity']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'owner',
            'name',
            'is_published',
            'total_likes',
            'created_at',
            'files',
        ]
