from django.db import models
from registration.models import Patient, Doctor, Hospital

# Create your models here.
class Appointment(models.Model):
    time = models.DateTimeField('appointment time')
    location = models.ForeignKey(Hospital)
    patient = models.ForeignKey(Patient, default=None)
    doctor = models.ForeignKey(Doctor)

    def get_absolute_url(self):
        return '/appointments/%i/' % self.id

    def __unicode__(self):
        return self.location
