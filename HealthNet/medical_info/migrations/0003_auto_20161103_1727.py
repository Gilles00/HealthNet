# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-03 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_info', '0002_auto_20161103_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='comments',
            field=models.CharField(default='', max_length=400),
        ),
    ]
