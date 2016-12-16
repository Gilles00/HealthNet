from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from registration.models import Patient, Doctor, Nurse, Hospital
from activity_log.models import Log
from django.utils import timezone

# Create your views here.
@login_required
def index(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        patient_list = Patient.objects.order_by('-user')
    except:
        doctor = None

    try:
        nurse = Nurse.objects.get(user=request.user)
        patient_list = Patient.objects.order_by('-user')
    except:
        nurse = None

    if nurse != None or doctor != None:
        return render(request, 'employee_admission_index.html', { 'patient_list':patient_list })
    else:
        patient = get_object_or_404(Patient, user=request.user)
        return render(request, 'patient_admission_index.html', { 'patient':patient })

@login_required
def view_patient(request, patient_id):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except:
        doctor = None

    try:
        nurse = Nurse.objects.get(user=request.user)
    except:
        nurse = None

    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'view_admission_status.html', { 'patient':patient, 'nurse':nurse, 'doctor':doctor })

@login_required
def admit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    try:
        nurse = Nurse.objects.get(user=request.user)
    except:
        nurse = None

    try:
        doctor = Doctor.objects.get(user=request.user)
    except:
        doctor = None

    if nurse != None:
        hospital = nurse.hospital
    else:
        hospital = doctor.hospital
    return render(request, 'admit.html', {'patient': patient, 'hospital': hospital})

@login_required
def discharge(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'discharge.html', {'patient': patient })

@login_required
def admit_redirect(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    try:
        nurse = Nurse.objects.get(user=request.user)
    except:
        nurse = None

    try:
        doctor = Doctor.objects.get(user=request.user)
    except:
        doctor = None

    if nurse != None:
        patient.admitted_hospital = nurse.hospital
        patient.save()
    else:
        patient.admitted_hospital = doctor.hospital
        patient.save()

    """ Activity Log Stuff """ 
    patUser = patient.user.username
    hospName = Hospital.__str__(patient.admitted_hospital)
    Log.create_log(Log, 
                   request.user.username, 
                   " admitted " + patUser + " to " + hospName + ".", 
                   timezone.now())
    """ Activity Log Stuff """ 
    return redirect('/admissions/')

@login_required
def discharge_redirect(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    """ Activity Log Stuff """ 
    patUser = patient.user.username
    hospName = Hospital.__str__(patient.admitted_hospital)
    Log.create_log(Log, 
                   request.user.username, 
                   " discharged " + patUser + " from " + hospName + ".", 
                   timezone.now())
    """ Activity Log Stuff """
    patient.admitted_hospital = None
    patient.save()
    return redirect('/admissions/')
