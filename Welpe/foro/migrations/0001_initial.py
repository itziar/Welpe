# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-10 12:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=150)),
                ('comentario', mezzanine.core.fields.RichTextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comentario',
                'verbose_name_plural': 'comentarios',
            },
        ),
    ]
