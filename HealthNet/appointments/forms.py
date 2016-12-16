from django import forms
from .models import Appointment
from registration.models import Patient, Doctor
from bootstrap3_datetime.widgets import DateTimePicker
from django.core.exceptions import ValidationError
from datetime import datetime

class UpdateAppointmentForm(forms.ModelForm):

    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
    time = forms.DateTimeField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm', 'pickSeconds': False}),
                               help_text='Choose a time on the quarters of an hour')

    class Meta:
        model = Appointment
        exclude = ['location', 'patient']

    def clean_time(self):
        time = self.cleaned_data['time']
        if int(time.minute) % 15 != 0:
            raise ValidationError("Appointment must be on the quarter of the hour!")
        elif Appointment.objects.filter(time=time).exists():
            raise ValidationError("The doctor already has an appointment at this time!")
        elif time.hour < 9 or time.hour >= 17:
            raise ValidationError("Hospital is not open at this time!")
        elif time < datetime.now():
            raise ValidationError("Can't pick a date in the past")

        return time

class UpdateAppointmentForm2(forms.ModelForm):

    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label=None)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
    time = forms.DateTimeField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm', 'pickSeconds': False}),
                               help_text='Choose a time on the quarters of an hour')

    class Meta:
        model = Appointment
        fields = ['time', 'location', 'patient', 'doctor']

    def clean_time(self):
        time = self.cleaned_data['time']
        if int(time.minute) % 15 != 0:
            raise ValidationError("Appointment must be on the quarter of the hour!")
        elif Appointment.objects.filter(time=time).exists():
            raise ValidationError("There is an appointment at this time!")
        elif time.hour < 9 or time.hour >= 17:
            raise ValidationError("Hospital is not open at this time!")
        elif time < datetime.now():
            raise ValidationError("Can't pick a date in the past")

        return time

class UpdateAppointmentForm3(forms.ModelForm):

    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label=None)
    time = forms.DateTimeField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm', 'pickSeconds': False}),
                               help_text='Choose a time on the quarters of an hour')

    class Meta:
        model = Appointment
        exclude = ['time', 'doctor']

    def clean_time(self):
        time = self.cleaned_data['time']
        if int(time.minute) % 15 != 0:
            raise ValidationError("Appointment must be on the quarter of the hour!")
        elif Appointment.objects.filter(time=time).exists():
            raise ValidationError("You already have an appointment at this time!")
        elif time.hour < 9 or time.hour >= 17:
            raise ValidationError("Hospital is not open at this time!")
        elif time < datetime.now():
            raise ValidationError("Can't pick a date in the past")

        return time

