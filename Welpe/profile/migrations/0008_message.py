# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-04 16:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile', '0007_auto_20170403_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(blank=True, max_length=150)),
                ('body', mezzanine.core.fields.RichTextField()),
                ('destinatario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='destinatario', to=settings.AUTH_USER_MODEL)),
                ('remitente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='remitente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]