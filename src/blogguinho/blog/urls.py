from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<post_slug>[-\w]+)/$', views.detail, name='post-detail'),
]
