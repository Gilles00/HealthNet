from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^view-patient/(?P<patient_id>[0-9]+)/$', views.view_patient),
    url(r'^admit/(?P<patient_id>[0-9]+)/$', views.admit),
    url(r'^discharge/(?P<patient_id>[0-9]+)/$', views.discharge),
    url(r'^admit-redirect/(?P<patient_id>[0-9]+)/$', views.admit_redirect),
    url(r'^discharge-redirect/(?P<patient_id>[0-9]+)/$', views.discharge_redirect),
]