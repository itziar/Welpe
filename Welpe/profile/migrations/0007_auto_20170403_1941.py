# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-03 17:41
from __future__ import unicode_literals

import Welpe.profile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_auto_20170403_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=Welpe.profile.models.user_directory_profile, verbose_name='Imagen'),
        ),
    ]
