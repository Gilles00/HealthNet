from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tests/(?P<test_id>[0-9]+)/$', views.test_detail, name='test_detail'),
    url(r'^prescriptions/(?P<rx_id>[0-9]+)/$', views.prescription_detail, name='prescription_detail'),
    url(r'^patientinfo/(?P<patient_id>[0-9]+)/$', views.doctor_view_of_patient),
    url(r'^add-prescription/(?P<patient_id>[0-9]+)/$', views.CreatePrescription.as_view()),
    url(r'^prescriptions/(?P<pk>[0-9]+)/delete/$', views.DeletePrescription.as_view()),
    url(r'^patientinfo/(?P<patient_id>[0-9]+)/medicalinfo/$', views.edit_medical),
    url(r'^patientinfo/(?P<patient_id>[0-9]+)/add-test/$', views.add_test),
    url(r'^tests/(?P<test_id>[0-9]+)/release-test/$', views.release_test),
    url(r'^transfer-patient/(?P<patient_id>[0-9]+)/$', views.transfer_patient)
]