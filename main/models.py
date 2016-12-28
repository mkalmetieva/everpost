from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256, default='')
    text = models.TextField(max_length=16392, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey('auth.User')

    def __str__(self):
        return self.title


class NicEditImage(models.Model):
    image = models.ImageField(upload_to='nicedit/')


class Comment(models.Model):
    text = models.TextField(max_length=4096, default='')
    parent_comment = models.ForeignKey('main.Comment', null=True)
    post = models.ForeignKey('main.Post')
    author = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
