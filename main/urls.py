from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from rest_framework import routers

from main import views
from main.rest_views import PostCommentsView, CommentsViewSet
from main.views import nicedit_upload

router = routers.DefaultRouter()
router.register(r'comments', CommentsViewSet, base_name='comments'),
# router.register(r'^api/comments/(?P<pk>[0-9]+)/$', CommentsViewSet.as_view{''}, base_name='delete_comment'),

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', views.RegisterFormView.as_view(), {'redirect_authenticated_user': True}, name='register'),
    url(r'^$', views.get_recent_posts, name='index'),
    url(r'^posts/$', views.get_recent_posts, name='recent_posts'),
    url(r'^user/(?P<pk>[0-9]+)/posts/$', views.get_user_posts, name='user_posts'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.view_post, name='post_view'),
    url(r'^post/add/$', views.add_post, name='post_add'),
    url(r'^post/edit/(?P<pk>[0-9]+)/$', views.edit_post, name='post_edit'),
    url(r'^post/delete/(?P<pk>[0-9]+)/$', views.delete_post, name='post_delete'),

    url(r'^upload/$', nicedit_upload, name='nicedit_upload'),

    url(r'^api/', include(router.urls)),
    url(r'^api/post/(?P<post_pk>.+)/comments$', PostCommentsView.as_view(), name='post_comments'),
]
