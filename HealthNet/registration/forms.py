from django import forms
from django.contrib.auth.forms import UserCreationForm

from bootstrap3_datetime.widgets import DateTimePicker
from .models import Patient, Doctor, Hospital

from activity_log.models import Log
from django.utils import timezone


class PatientCreationForm(UserCreationForm):
    '''
    Extension of UserCreationForm to support fields needed by our patient model
    '''
    dateOfBirth = forms.DateTimeField(label='Date of Birth',
                                      help_text='Format: MM/DD/YYYY',
                                      widget=DateTimePicker(options={'format': 'YYYY-MM-DD',
                                                                     'pickTime': False})
                                     )
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    height = forms.FloatField(help_text='Enter your height in feet')
    weight = forms.FloatField(help_text='Enter your weight in pounds')
    insurer = forms.CharField(max_length=20)
    address = forms.CharField(max_length=30)


    def __init__(self, *args, **kwargs):
        super(PatientCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(PatientCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        '''
        Log registration.
        '''
        Log.create_log(Log, user.username, " registered as a Patient.", timezone.now())
        
        try: 
            patient = Patient(user=user,
                              dateOfBirth=self.cleaned_data.get('dateOfBirth'),
                              height=self.cleaned_data.get('height'),
                              weight=self.cleaned_data.get('weight'),
                              insurer=self.cleaned_data.get('insurer'),
                              address=self.cleaned_data.get('address'),
                              admitted_hospital=None
                              )
        except:
            # patient creation failed. Delete the user so they can try again
            user.delete()

        if commit:
            patient.save()
        return patient
