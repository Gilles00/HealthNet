# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-15 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_opened',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
