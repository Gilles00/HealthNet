from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.send_message),
    url(r'^view/(?P<msg_id>[0-9]+)$', views.view_message),
    url(r'^inbox/', views.view_inbox)
]