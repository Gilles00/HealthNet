# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-04 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]
