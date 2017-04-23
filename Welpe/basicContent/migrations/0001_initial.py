# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-10 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('basicModels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.FileField(upload_to=b'contentFiles')),
                ('fileSummary', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='BasicContent',
            fields=[
                ('genericcontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='basicModels.GenericContent')),
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page', 'basicModels.genericcontent', models.Model),
        ),
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('nameToShow', models.CharField(max_length=500)),
                ('externalLink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ext_links', to='basicContent.BasicContent')),
            ],
        ),
        migrations.AddField(
            model_name='attachedfile',
            name='attachedFile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='att_files', to='basicContent.BasicContent'),
        ),
    ]
