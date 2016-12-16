from django.db import models
from django.contrib.auth.models import User
from registration.models import Patient, Doctor, Nurse
from medical_info.models import Prescription

# Create your models here.
class Log(models.Model):
    log_info = models.CharField(max_length=100, blank=True)
    date_time_logged = models.DateTimeField('date and time of activity', blank=True)
    username = models.CharField(max_length=150, blank=True)

    def create_log(cls, username, loginfo, datetimeinfo):
        log = cls(log_info=loginfo, date_time_logged=datetimeinfo, username=username)
        log.save()

    def __str__(self):
        return '{} | {}{}'.format(self.date_time_logged, self.username, self.log_info)

class Stat(models.Model):
    num_patients = models.IntegerField(blank=True)
    avg_weight = models.FloatField(blank=True)
    avg_height = models.FloatField(blank=True)
    prescriptions_per_patient = models.FloatField(blank=True)
    
    def patientStats():
        avgWeight = 0.0
        avgHeight = 0.0
        numPatients = 0
        prescriptionsPerPatient = 0

        for patient in Patient.objects.all():
            avgWeight = avgWeight + patient.weight
            avgHeight = avgHeight + patient.height
            numPatients = numPatients + 1

        if numPatients < 1:
            try:
                stat = Stat.objects.first()
                stat.num_patients = numPatients
                stat.avg_weight = 0
                stat.avg_height = 0
                stat.prescriptions_per_patient = 0
                stat.save()
            except: 
                stat = Stat(num_patients=numPatients, 
                           avg_weight=0, 
                           avg_height=0,
                           prescriptions_per_patient=0)
                stat.save()
        else:
            avgWeight = avgWeight / numPatients
            avgHeight = avgHeight / numPatients

            for prescription in Prescription.objects.all():
                prescriptionsPerPatient = prescriptionsPerPatient + 1

            prescriptionsPerPatient = prescriptionsPerPatient / numPatients

            try:
                stat = Stat.objects.first()
                stat.num_patients = numPatients
                stat.avg_weight = avgWeight
                stat.avg_height = avgHeight
                stat.prescriptions_per_patient = prescriptionsPerPatient
                stat.save()
            except: 
                stat = Stat(num_patients=numPatients, 
                           avg_weight=avgWeight, 
                           avg_height=avgHeight, 
                           prescriptions_per_patient=prescriptionsPerPatient)
                stat.save()
