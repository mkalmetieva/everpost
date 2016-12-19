from django.conf.urls import url
from django.contrib.auth.views import login, logout

from main import views

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', views.RegisterFormView.as_view(), {'redirect_authenticated_user': True}, name='register'),
    url(r'', views.get_recent_posts, name='index'),
    url(r'^posts/', views.get_recent_posts, name='recent_posts'),
    url(r'^user/(?P<key>[0-9]+)/posts/$', views.get_recent_posts, name='user_posts'),
    url(r'^post/(?P<key>[0-9]+)/$', views.view_post, name='post_view'),
    url(r'^note/add/$', views.add_post, name='post_add'),
    url(r'^note/edit/(?P<key>[0-9]+)/$', views.edit_post, name='post_edit'),
    url(r'^note/delete/(?P<key>[0-9]+)/$', views.delete_post, name='post_delete')
]
