from django.contrib import admin
from .models import Log, Stat

class LogAdmin(admin.ModelAdmin):
    fields = ['log_info', 'date_time_logged', 'username']
    list_display = ( 'username', 'log_info', 'date_time_logged')

class StatAdmin(admin.ModelAdmin):
    fields = ['num_patients', 'avg_weight', 'avg_height', 'prescriptions_per_patient']
    list_display = ['num_patients', 'avg_weight', 'avg_height', 'prescriptions_per_patient']

# Register your models here.
admin.site.register(Log, LogAdmin)
admin.site.register(Stat, StatAdmin)