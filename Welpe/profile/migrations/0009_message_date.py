# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-04 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default='1970-01-01 00:00'),
            preserve_default=False,
        ),
    ]