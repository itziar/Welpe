# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-01 09:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ofertaTrabajo', '0002_commentsoferta_anonimo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentsoferta',
            name='oferta',
        ),
        migrations.RemoveField(
            model_name='commentsoferta',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='CommentsOferta',
        ),
    ]