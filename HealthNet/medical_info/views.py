from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.utils.decorators import method_decorator

from registration.models import Patient, Doctor, Nurse
from activity_log.models import Log, Stat
from django.utils import timezone
from .models import Test, Prescription
from .forms import PrescriptionForm, MedicalInfoForm, AddTestForm, ReleaseTestForm
# Create your views here.
@login_required
def index(request):
    try:
        patient = Patient.objects.filter(user=request.user).first()
        testlist =  Test.objects.filter(patient=patient)
        rxlist = Prescription.objects.filter(patient=patient)
    except:
        patient = None

    try:
        doctor = Doctor.objects.filter(user=request.user).first()
        patientlist = Patient.objects.order_by('-user')
    except:
        doctor = None

    try:
        nurse = Nurse.objects.filter(user=request.user).first()
        patientlist = Patient.objects.filter(admitted_hospital=nurse.hospital).order_by('-user')
    except:
        nurse = None

    Stat.patientStats()

    if nurse != None:
        return render(request, 'nurse_index.html', {'patient_list': patientlist})
    elif doctor != None:
        return render(request, 'doctor_index.html', {'patient_list': patientlist})
    else:
        return render(request, 'patient_index.html', {'patient': patient, 'testlist': testlist, 'rxlist': rxlist})

@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    try:
        doctor = Doctor.objects.filter(user=request.user)
    except:
        doctor = None

    return render(request, 'test_detail.html', {'test': test, 'doctor': doctor})

@login_required
def prescription_detail(request, rx_id):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except:
        doctor = None

    rx = get_object_or_404(Prescription, pk=rx_id)
    return render(request, 'prescription_detail.html', {'rx': rx, 'doctor': doctor})

@login_required
def doctor_view_of_patient(request, patient_id):
    try:
        doctor = Doctor.objects.filter(user=request.user).first()
    except:
        doctor = None

    patient = get_object_or_404(Patient, pk=patient_id)
    testlist = Test.objects.filter(patient=patient)
    rxlist = Prescription.objects.filter(patient=patient)

    return render(request, 'view_patient.html', {'testlist': testlist, 'rxlist': rxlist, 'doctor': doctor, 'patient': patient})

@login_required
def edit_medical(request, patient_id):
    if request.method == 'POST':
        form = MedicalInfoForm(request.POST)

        if form.is_valid():
            patient = Patient.objects.get(pk=patient_id)
            patient.height = form.cleaned_data['height']
            patient.weight = form.cleaned_data['weight']
            patient.save()

            log_message = " updated user " + patient.user.username + "'s medical information." 
            Log.create_log(Log, request.user.username, log_message, timezone.now())
            Stat.patientStats()

            return redirect('/medicalinfo/patientinfo/' + patient_id)

    else:
        form = MedicalInfoForm()

    return render(request, 'edit_medical.html', {'form': form})

@login_required
def transfer_patient(request, patient_id):
    if request.method == 'POST':
        doctor = Doctor.objects.get(user=request.user)
        patient = Patient.objects.get(pk=patient_id)
        patient.admitted_hospital = doctor.hospital
        patient.save()

        log_message = " transferred user " + patient.user.username + " to " + doctor.hospital.name + "."
        Log.create_log(Log, request.user.username, log_message , timezone.now())

        return redirect('/medicalinfo/')

    return render(request, 'transfer_patient.html') 

@login_required
def add_test(request, patient_id):
    if request.method == 'POST':
        form = AddTestForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = Patient.objects.get(pk=patient_id)
            obj.result = 'Pending'
            obj.comments = ''
            obj.save() 
            Log.create_log(Log, 
                   request.user.username, 
                   " created test for " + obj.patient.user.username + ".", 
                   timezone.now())
            return redirect('/medicalinfo/patientinfo/' + patient_id)

    else:
        form = AddTestForm()

    return render(request, 'add_test.html', {'form': form})

@login_required
def release_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    if request.method == 'POST':
        form = ReleaseTestForm(request.POST)

        if form.is_valid():
            if test.patient.admitted_hospital != doctor.hospital:
                error = "Cannot release " + test.name + ". Patient is not in " + doctor.hospital.name + "."
                return render(request, 'error.html', {'error':error})

            obj = form.save(commit=False)
            test.result = obj.result
            test.comments = obj.comments
            test.save()
            Log.create_log(Log, 
                   request.user.username, 
                   " released test for " + test.patient.user.username + ".", 
                   timezone.now())
            return redirect('/medicalinfo/')

    else:
        form = ReleaseTestForm()

    return render(request, 'release_test.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class CreatePrescription(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'add_prescription.html'
    success_url = '/medicalinfo/'

    def get_initial(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get('patient_id'))
        return {
            'patient': patient
        }

@method_decorator(login_required, name='dispatch')
class DeletePrescription(DeleteView):
    model = Prescription
    template_name = 'delete_prescription.html'
    success_url = '/medicalinfo/'

