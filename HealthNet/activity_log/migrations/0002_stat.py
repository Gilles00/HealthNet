# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-06 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_patients', models.IntegerField(blank=True)),
                ('avg_weight', models.FloatField(blank=True)),
                ('avg_height', models.FloatField(blank=True)),
                ('prescriptions_per_patient', models.FloatField(blank=True)),
            ],
        ),
    ]
