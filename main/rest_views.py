from datetime import datetime, timedelta

from django.db import transaction
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from main.models import Comment, Post
from main.serializers import CommentSerializer, PostSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        dateVal = self.kwargs['date']
        dateMin = datetime.strptime(dateVal, '%d-%m-%Y').date()
        dateMax = dateMin + timedelta(days=1)
        return Post.objects.filter(created_at__gte=dateMin, created_at__lt=dateMax
                                   ).order_by('created_at')


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @transaction.atomic
    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied
        self.queryset.filter(parent_comment=instance).update(parent_comment_id=None)
        instance.delete()


class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk']).order_by('created_at')
