from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import Post, Comment


class UserNameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username')

    def get_validation_exclusions(self):
        exclusions = super(UserNameSerializer, self).get_validation_exclusions()
        return exclusions + ['username']


class PostSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(many=False, read_only=True)
    parent_comment = serializers.CharField(source='parent_comment.id', required=False, allow_null=True)
    post = serializers.CharField(source='post.id')
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'parent_comment', 'created_at', 'post')

    def get_validation_exclusions(self):
        exclusions = super(CommentSerializer, self).get_validation_exclusions()
        return exclusions + ['created_at', 'parent_comment', 'author']

    def create(self, validated_data):
        parent_comment_id = validated_data['parent_comment']['id']
        del validated_data['parent_comment']
        post_id = validated_data['post']['id']
        del validated_data['post']

        comment = Comment(**validated_data)
        if parent_comment_id:
            comment.parent_comment_id = parent_comment_id
        if post_id:
            comment.post_id = post_id
        comment.save()
        return comment


class UserPostStatisticsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    count = serializers.IntegerField()
