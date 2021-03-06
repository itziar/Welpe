# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-29 06:41
from __future__ import unicode_literals

import Welpe.actividades.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actividades', '0006_auto_20170501_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsPrivados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=150)),
                ('comentario', mezzanine.core.fields.RichTextField()),
                ('anonimo', models.BooleanField(default=False)),
                ('archivo', models.FileField(blank=True, null=True, upload_to=Welpe.actividades.models.user_directory_comments_reg)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.Actividades')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comentario',
                'verbose_name_plural': 'comentarios',
            },
        ),
    ]
