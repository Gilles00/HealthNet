from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PatientCreationForm
from django.contrib.auth import logout 
from activity_log.models import Log, Stat
from django.utils import timezone

def index(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            Stat.patientStats()
            return redirect('/login')
    else:
        form = PatientCreationForm()
            
    return render(request,
                  'register.html',
                  {'form': form})

def logout_view(request):
    Log.create_log(Log, request.user.username, " has logged out.", timezone.now())
    logout(request)
    return redirect('/login')
