# community/board/serializers.py

from rest_framework import serializers
from .models import Post, Comment
from .models import Facility

class PostSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.profile.nickname', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.profile.nickname', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'comment', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True}
        }

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name', 'region', 'location', 'sport', 'target', 'period', 'day', 'time', 'fee', 'capacity']
