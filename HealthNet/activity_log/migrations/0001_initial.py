# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_info', models.CharField(blank=True, max_length=100)),
                ('date_time_logged', models.DateTimeField(blank=True, verbose_name='date and time of activity')),
                ('username', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]
