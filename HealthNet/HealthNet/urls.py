"""HealthNet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from appointments.views import index

urlpatterns = [
    url(r'^$', index, name='appointments'),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^register/', include('registration.urls')),
    url(r'^appointments/', include('appointments.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('account_profile.urls')),
    url(r'^activitylog/', include('activity_log.urls')),
    url(r'^medicalinfo/', include('medical_info.urls')),
    url(r'^messages/', include('private_messages.urls')),
    url(r'^admissions/', include('admissions.urls'))
]
