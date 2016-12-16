from django.conf.urls import url

from . import views
from .views import CreateAppointment, DeleteAppointment

urlpatterns = [
    url(r'^view/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$', views.view_cal_at, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<appointment_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<appointment_id>[0-9]+)/edit/$', views.patient_edit, name='edit'),
    url(r'^(?P<appointment_id>[0-9]+)/doctor-edit/$', views.doctor_edit, name='edit'),
    url(r'^(?P<appointment_id>[0-9]+)/nurse-edit/$', views.nurse_edit, name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', DeleteAppointment.as_view(), name='delete'),
    url(r'^schedule/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/', views.patient_schedule),
    url(r'^available/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<hour>[0-9]+)/(?P<minute>[0-9]+)/$',
        views.patient_availabilities, name='available'),
    url(
        r'^confirm/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<hour>[0-9]+)/(?P<minute>[0-9]+)/(?P<doc_id>[0-9]+)/$',
        views.confirm),
    url(r'^create/$', CreateAppointment.as_view(), name='create'),
    url(r'^redirect/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<hour>[0-9]+)/(?P<minute>[0-9]+)/(?P<doc_id>[0-9]+)/$', views.patient_redirect)
]
