# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-31 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='registration.Hospital'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nurse',
            name='hospital',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='registration.Hospital'),
            preserve_default=False,
        ),
    ]
