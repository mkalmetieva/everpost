from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import Post, Comment


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'author', 'rating')


class CommentSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()
    parent_comment = serializers.CharField(source='parent_comment.id')
    created_at = serializers.DateTimeField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'parent_comment', 'created_at')
