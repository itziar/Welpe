# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-20 17:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('propuestas', '0002_remove_propuestas_titulo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ofertaTrabajo', '0002_commentsoferta_anonimo'),
        ('infoInteres', '0001_initial'),
        ('actividades', '0003_auto_20161210_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.Actividades')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infoInteres.InfoInteres')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikeOferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofertaTrabajo.OfertaTrabajo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikePropuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='propuestas.Propuestas')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grado', models.TextField(blank=True, max_length=150)),
                ('curso', models.IntegerField()),
                ('dni', models.TextField(blank=True, max_length=15)),
                ('bio', mezzanine.core.fields.RichTextField()),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('show_email', models.BooleanField(default=False, verbose_name='mostrar email')),
                ('photo', mezzanine.core.fields.FileField(blank=True, max_length=255, null=True, verbose_name='Photo')),
                ('telefono', models.TextField(max_length=15)),
                ('pagina_web', models.URLField()),
                ('id_skype', models.TextField(max_length=50)),
                ('institucion', models.TextField(max_length=150)),
                ('departamento', models.TextField(max_length=150)),
                ('puesto', models.TextField(max_length=150)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
