from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=200)
    result = models.CharField(max_length=20, default='Pending')
    comments = models.CharField(max_length=400, default='')
    date = models.DateTimeField('test time')
    patient = models.ForeignKey('registration.Patient')

    def is_pending(self):
        return self.result == 'Pending'

class Prescription(models.Model):
    name = models.CharField(max_length=100)
    dosage_info = models.CharField(max_length=200)
    patient = models.ForeignKey('registration.Patient')
