# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-16 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertaTrabajo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsoferta',
            name='anonimo',
            field=models.BooleanField(default=False),
        ),
    ]
