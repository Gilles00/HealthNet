# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-15 03:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0002_message_is_opened'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='reciever',
            new_name='recipient',
        ),
    ]
