from django.conf.urls import url 

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit-patient/$', views.edit_patient, name='edit-patient'),
    url(r'^edit-doctor/$', views.edit_doctor, name='edit-doctor'),
    url(r'^edit-nurse/$', views.edit_nurse, name='edit-nurse')
]
