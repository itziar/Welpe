# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('columns', models.CharField(default=b'3', max_length=1, choices=[(b'6', b'Two columns'), (b'4', b'Three columns'), (b'3', b'Four Columns')])),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Portfolio',
                'verbose_name_plural': 'Portfolios',
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='PortfolioItem',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('layout', models.PositiveIntegerField(default=1, choices=[(1, b'Slideshow/video above, content below'), (2, b'Slideshow/video on left, content on right'), (3, b'Slideshow/video on right, content on left')])),
                ('description_heading', models.CharField(default=b'Project description', max_length=200)),
                ('featured_image', mezzanine.core.fields.FileField(max_length=255, null=True, verbose_name='Featured Image', blank=True)),
                ('featured_video', models.TextField(help_text=b'Optional, putting video embed code (iframe) here, will override a Featured image specified above.  This has been tested to work with Youtube and Vimeo, but may work with other iframes as well.', blank=True)),
                ('details_heading', models.CharField(default=b'Project details', max_length=200)),
                ('website', models.CharField(help_text=b'A link to the finished project or clients website  (optional)', max_length=2000, blank=True)),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Portfolio item',
                'verbose_name_plural': 'Portfolio items',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='PortfolioItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Portfolio Item Category',
                'verbose_name_plural': 'Portfolio Item Categories',
            },
        ),
        migrations.CreateModel(
            name='PortfolioItemDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=100)),
                ('portfolioitem', models.ForeignKey(related_name='details', to='portfolio.PortfolioItem')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='PortfolioItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('file', mezzanine.core.fields.FileField(max_length=200, verbose_name='File')),
                ('alt_text', models.CharField(max_length=200, blank=True)),
                ('portfolioitem', models.ForeignKey(related_name='images', to='portfolio.PortfolioItem')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.AddField(
            model_name='portfolioitem',
            name='categories',
            field=models.ManyToManyField(related_name='portfolioitems', verbose_name='Categories', to='portfolio.PortfolioItemCategory', blank=True),
        ),
        migrations.AddField(
            model_name='portfolioitem',
            name='related_items',
            field=models.ManyToManyField(related_name='related_items_rel_+', to='portfolio.PortfolioItem', blank=True),
        ),
    ]
