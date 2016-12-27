from rest_framework.generics import ListAPIView

from main.models import Comment
from main.serializers import CommentSerializer


class CommentsViewSet(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk']).order_by('created_at')
