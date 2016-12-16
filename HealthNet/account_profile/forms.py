from django import forms
from django.forms import ModelForm
from registration.models import Doctor, Patient, Nurse
from bootstrap3_datetime.widgets import DateTimePicker

class UpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        dateOfBirth = forms.DateTimeField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm', 'pickSeconds': False}))
        fields = ['dateOfBirth', 'height', 'weight', 'insurer', 'address']

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty', 'hospital']

class UpdateNurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['hospital']
