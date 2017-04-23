# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpost_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('file', mezzanine.core.fields.FileField(max_length=200, verbose_name='File')),
                ('alt_text', models.CharField(max_length=200, blank=True)),
                ('blog_post', models.ForeignKey(related_name='images', to='blog.BlogPost')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Slideshow (will only display if a featured video is not specified above).  If no featured image is selected above the first image added will become the featured image.',
                'verbose_name_plural': 'Slideshow (will only display if a featured video is not specified above).  If no featured image is selected above the first image added will become the featured image.',
            },
        ),
    ]
