from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256, default='')
    text = models.TextField(max_length=65536, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey('auth.User', default=None)

    def __str__(self):
        return self.title
