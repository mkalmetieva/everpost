from django.conf.urls import url
from django.contrib.auth.views import login, logout

from main.views import index, register_user

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register_user, name='register'),
    url(r'', index, name='index'),
    url(r'^recipes/', login, {'template_name': 'recipes_search.html'}, name='recipes_search'),
]
