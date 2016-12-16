from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Appointment
from .forms import UpdateAppointmentForm, UpdateAppointmentForm2, UpdateAppointmentForm3
from django.views.generic.edit import DeleteView, CreateView
from bootstrap3_datetime.widgets import DateTimePicker

from activity_log.models import Log, Stat
from django.utils import timezone
from registration.models import Patient, Doctor, Nurse

from calendar import Calendar
from datetime import date, time, datetime

@login_required
def index(request):

    appointment_list = Appointment.objects.all()
    try: 
        patient = Patient.objects.get(user=request.user)
        appointment_list = Appointment.objects.filter(patient=patient).order_by('-time')[:5]
    except:
        patient = None

    try:
        doctor = Doctor.objects.get(user=request.user)
        appointment_list = Appointment.objects.filter(doctor=doctor).order_by('-time')[:5]
    except:
        doctor = None


    today = date.today()
    calendar = Calendar(firstweekday=6)
    iter =  calendar.monthdatescalendar(today.year, today.month)
    month = today.strftime("%B")

    checkyearlast = today.year
    checkyearnext = today.year
    lastmonth = today.month - 1
    if lastmonth == 0:
        lastmonth = 12
        checkyearlast = checkyearlast - 1

    nextmonth = today.month + 1
    if nextmonth == 13:
        nextmonth = 1
        checkyearnext = checkyearnext + 1

    context = {
        'appointment_list': appointment_list,
        'iter': iter,
        'month': month,
        'today': today,
        'nextmonth':nextmonth,
        'nextyear':checkyearnext,
        'lastmonth':lastmonth,
        'lastyear':checkyearlast,
        'markdate':today
    }

    Stat.patientStats()

    if doctor is not None:
        return render(request, 'doctor_appointment_index.html', context)
    if patient is not None:
        return render(request, 'patient_appointment_index.html', context)

    return render(request, 'nurse_appointment_index.html', {'apps':appointment_list})

@login_required
def view_cal_at(request, year, month):
    appointment_list = Appointment.objects.order_by('-time')[:5]
    try:
        patient = Patient.objects.get(user=request.user)
        appointment_list = appointment_list.filter(patient=patient).order_by('-time')[:5]
    except:
        patient = None

    try:
        doctor = Doctor.objects.get(user=request.user)
        appointment_list = Appointment.objects.filter(doctor=doctor).order_by('-time')[:5]
    except:
        doctor = None

    markdate = date(int(year), int(month), 1)
    iter = Calendar(firstweekday=6).monthdatescalendar(int(year), int(month))
    month = markdate.strftime("%B")
    today = date.today()



    checkyearlast = markdate.year
    checkyearnext = markdate.year
    lastmonth = markdate.month - 1
    if lastmonth == 0:
        lastmonth = 12
        checkyearlast = checkyearlast - 1

    nextmonth = markdate.month + 1
    if nextmonth == 13:
        nextmonth = 1
        checkyearnext = checkyearnext + 1

    context = {
        'appointment_list': appointment_list,
        'iter': iter,
        'month': month,
        'today': today,
        'nextmonth': nextmonth,
        'nextyear': checkyearnext,
        'lastmonth': lastmonth,
        'lastyear': checkyearlast,
        'markdate': markdate
    }

    if doctor is not None:
        return render(request, 'doctor_appointment_index.html', context)
    if patient is not None:
        return render(request, 'patient_appointment_index.html', context)

    return render(request, 'nurse_appointment_index.html', {'apps':appointment_list})

@login_required
def patient_schedule(request, year, month, day):
    times = []
    lists = []

    selected_date = date(int(year), int(month), int(day))

    open = time(hour=9, tzinfo=timezone.now().tzinfo)
    close = time(hour=17, tzinfo=timezone.now().tzinfo)
    while open < close:
        times.append(time(hour=open.hour, minute=open.minute))
        a_list = []
        for doc in Doctor.objects.all():
            try:
                Appointment.objects.get(doctor=doc, time=datetime.combine(selected_date, open))
            except ObjectDoesNotExist:
                a_list.append(doc)

        lists.append(a_list)

        h_inc = open.hour
        m_inc = open.minute + 15
        if m_inc == 60:
            h_inc += 1
            m_inc = 0

        open = open.replace(hour=h_inc, minute=m_inc)


    context = zip(times, lists)
    return render(request, "schedule.html", {'context':context, 'date':selected_date})

@login_required
def patient_availabilities(request, year, month, day, hour, minute):
    selected_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), tzinfo=timezone.now().tzinfo)
    d_list = None
    for doc in Doctor.objects.all():
        try:
            Appointment.objects.get(doctor=doc, time=selected_time)
        except:
            if d_list is None:
                d_list = []

            d_list.append(doc)

    return render(request, 'availabilities.html', {'list':d_list, 'date':selected_time})

@login_required
def confirm(request, year, month, day, hour, minute, doc_id):
    doctor = get_object_or_404(Doctor, id=doc_id)
    app_date = date(int(year), int(month), int(day))
    app_time = time(hour=int(hour), minute=int(minute))

    context = {
        'doctor':doctor,
        'date':app_date,
        'time':app_time
    }
    return render(request, 'confirm.html', context)

@login_required
def patient_redirect(request, year, month, day, hour, minute, doc_id):
    app_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), tzinfo=timezone.now().tzinfo)
    doctor = get_object_or_404(Doctor, id=doc_id)
    app = Appointment(time=app_time, location=doctor.hospital, doctor=doctor, patient=get_object_or_404(Patient, user=request.user))
    app.save()

    Log.create_log(Log, 
                   request.user.username, 
                   " scheduled an appointment with " + doctor.user.username + ".",
                   timezone.now())

    return redirect('/appointments/')

@login_required
def detail(request, appointment_id):
    try:
        nurse = Nurse.objects.filter(user=request.user).first()
    except:
        nurse = None

    try:
        doctor = Doctor.objects.filter(user=request.user).first()
    except:
        doctor = None

    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        raise Http404("Appointment does not exist")


    return render(request, 'detail.html', {'appointment': appointment, 'doctor':doctor, 'nurse':nurse})

class DeleteAppointment(DeleteView):
    model = Appointment
    template_name = 'delete.html'
    success_url = '/appointments/'

    def delete(self, request, *args, **kwargs):
        Log.create_log(Log,
                       request.user.username,
                       " has deleted one of their appointments.",
                       timezone.now())
        return super().delete(request, *args, **kwargs)

class CreateAppointment(CreateView):
    model = Appointment
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label=None)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
    time = forms.DateTimeField
    template_name = 'create.html'
    success_url = '/appointments/'
    fields = ['time', 'location', 'patient', 'doctor']

    def get_form(self, form_class=UpdateAppointmentForm2):
        form = super(CreateAppointment, self).get_form(form_class)
        form.fields['time'].widget = DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm', 'pickSeconds': False})
        return form

@login_required
def patient_edit(request, appointment_id):
    instance = get_object_or_404(Appointment, id=appointment_id)
    form = UpdateAppointmentForm(request.POST, instance=instance)
    if form.is_valid():


        obj = form.save(commit=False)
        obj.patient = get_object_or_404(Patient, user=request.user)
        obj.location = obj.doctor.hospital
        obj.save()
        Log.create_log(Log,
                       request.user.username,
                       " has updated one of their appointments.",
                       timezone.now())
        return redirect('/appointments')

    return render(request, 'edit.html', {'form': form})

@login_required
def doctor_edit(request, appointment_id):
    instance = get_object_or_404(Appointment, id=appointment_id)
    form = UpdateAppointmentForm3(request.POST, instance=instance)
    if form.is_valid():


        obj = form.save(commit=False)
        obj.doctor = get_object_or_404(Doctor, user=request.user)
        obj.location = obj.doctor.hospital
        obj.save()
        Log.create_log(Log,
                       request.user.username,
                       " has updated one of their appointments.",
                       timezone.now())
        return redirect('/appointments')

    return render(request, 'edit.html', {'form': form})

@login_required
def nurse_edit(request, appointment_id):
    instance = get_object_or_404(Appointment, id=appointment_id)
    form = UpdateAppointmentForm2(request.POST, instance=instance)
    if form.is_valid():

        obj = form.save(commit=False)
        obj.save()
        Log.create_log(Log,
                       request.user.username,
                       " has updated one of their appointments.",
                       timezone.now())
        return redirect('/appointments')

    return render(request, 'edit.html', {'form': form})



