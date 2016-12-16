from django.db import models
from django.contrib.auth.models import User
from medical_info.models import Test

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateTimeField('date of birth', blank=True)
    height = models.FloatField(blank=True)
    weight = models.FloatField(blank=True)
    insurer = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=30, blank=True)
    admitted_hospital = models.ForeignKey(Hospital, null=True, related_name='admitted')

    def __str__(self):
        return User.get_full_name(self.user)

    def htmlName(self):
        return User.get_full_name(self.user)

    def get_absolute_url(self):
        return '/profile/'

    def get_tests(self):
        return Test.objects.filter(patient=self, result='Pending')

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    specialty = models.CharField(max_length=20)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return User.get_full_name(self.user)

    def htmlName(self):
        return User.get_full_name(self.user)

    def get_absolute_url(self):
        return '/profile/'

class Nurse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return User.get_full_name(self.user)

    def htmlName(self):
        return User.get_full_name(self.user)

    def get_absolute_url(self):
        return '/profile';

