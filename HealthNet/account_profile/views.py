from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from registration.models import Patient, Doctor, Nurse
from .forms import UpdatePatientForm, UpdateDoctorForm, UpdateNurseForm
from django.views.generic import UpdateView

from activity_log.models import Log, Stat
from django.utils import timezone

from django.shortcuts import render, redirect

# Create your views here.

@login_required
def index(request):
    try: 
        patient = Patient.objects.get(user=request.user)
    except:
        patient = None
    try:
        doctor = Doctor.objects.get(user=request.user)
    except:
        doctor = None
    try:
        nurse = Nurse.objects.get(user=request.user)
    except:
        nurse = None

    if patient:
        context = {
            'patient': patient
        }
    elif doctor:
        context = {
            'doctor': doctor
        }
    else:
        context = {
            'nurse': nurse
        }
    return render(request, 'account_profile/index.html', context)

@login_required
def edit_patient(request):
    instance = Patient.objects.get(user=request.user)
    form = UpdatePatientForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        Stat.patientStats()
        Log.create_log(Log, 
                       request.user.username, 
                       " has updated their profile.", 
                       timezone.now())

        return redirect('/profile')

    return render(request, 
                  'edit.html',
                  {'form': form})     


@login_required
def edit_doctor(request):
    instance = Doctor.objects.filter(user=request.user).first()
    form = UpdateDoctorForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        Log.create_log(Log, request.user.username, " has updated their profile.", timezone.now())
        return redirect('/profile')
    return render(request, 'edit.html', {'form': form})

@login_required
def edit_nurse(request):
    instance = Nurse.objects.filter(user=request.user).first()
    form = UpdateNurseForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        Log.create_log(Log, request.user.username, " has updated their profile.", timezone.now())
        return redirect('/profile')
    return render(request, 'edit.html', {'form': form})
