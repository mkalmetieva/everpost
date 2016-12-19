from django.conf.urls import url
from django.contrib.auth.views import login, logout

from main.views import index, RegisterFormView

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', RegisterFormView.as_view(), name='register'),
    url(r'', index, name='index'),
    url(r'^posts/', login, {'template_name': 'recent_posts.html'}, name='recent_posts'),
]
