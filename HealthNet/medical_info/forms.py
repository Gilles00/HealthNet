from django import forms
from django.db import models
from .models import Prescription, Test
from registration.models import Patient
from bootstrap3_datetime.widgets import DateTimePicker

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['name', 'dosage_info', 'patient']

class AddTestForm(forms.ModelForm):

    date = forms.DateTimeField(label='Date of Test',
                                      help_text='Format: MM/DD/YYYY',
                                      widget=DateTimePicker(options={'format': 'YYYY-MM-DD',
                                                                     'pickTime': False})
                                )

    class Meta:
        model = Test
        exclude = ['result', 'comments', 'patient']

class ReleaseTestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ['name', 'date', 'patient']

class MedicalInfoForm(forms.Form):
    height = forms.FloatField(help_text='Enter your height in feet')
    weight = forms.FloatField(help_text='Enter your weight in pounds')

