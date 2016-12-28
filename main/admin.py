from django.contrib import admin

from main.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at')
    search_fields = ('author__username', 'text')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
