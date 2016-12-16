from django.shortcuts import render
from activity_log.models import Log

# Create your views here.

def index(request):
    log_list = Log.objects.order_by('-date_time_logged')[:100]
    context = {
        'log_list': log_list
    }
    return render(request, 'activity_log/index.html', context)