# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.extensions
import feincms.module.medialibrary.fields
from django.conf import settings
import django.utils.timezone
import feincms.module.mixins
import feincms.contrib.richtext
import feincms.translations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medialibrary', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ordering', models.SmallIntegerField(default=0, verbose_name='ordering')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['ordering'],
                'verbose_name': 'category',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=10, choices=[('de', 'German')], default='de', verbose_name='language', editable=False)),
                ('title', models.CharField(verbose_name='category title', max_length=100)),
                ('slug', models.SlugField(verbose_name='slug', unique=True)),
                ('description', models.CharField(blank=True, verbose_name='description', max_length=250)),
                ('parent', models.ForeignKey(to='elephantblog.Category')),
            ],
            options={
                'verbose_name_plural': 'category translations',
                'ordering': ['title'],
                'verbose_name': 'category translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='is active')),
                ('is_featured', models.BooleanField(default=False, db_index=True, verbose_name='is featured')),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('slug', models.SlugField(unique_for_date='published_on', verbose_name='slug', max_length=100)),
                ('published_on', models.DateTimeField(blank=True, db_index=True, null=True, help_text='Will be filled in automatically when entry gets published.', verbose_name='published on', default=django.utils.timezone.now)),
                ('last_changed', models.DateTimeField(auto_now=True, verbose_name='last change')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('categories', models.ManyToManyField(null=True, to='elephantblog.Category', blank=True, verbose_name='categories')),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['-published_on'],
                'get_latest_by': 'published_on',
                'verbose_name': 'entry',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
        migrations.CreateModel(
            name='MediaFileContent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('type', models.CharField(choices=[('default', 'default')], default='default', verbose_name='type', max_length=20)),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile', verbose_name='media file')),
                ('parent', models.ForeignKey(to='elephantblog.Entry')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'media file',
                'abstract': False,
                'verbose_name_plural': 'media files',
                'db_table': 'elephantblog_entry_mediafilecontent',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', feincms.contrib.richtext.RichTextField(blank=True, verbose_name='text')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(to='elephantblog.Entry')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'rich text',
                'abstract': False,
                'verbose_name_plural': 'rich texts',
                'db_table': 'elephantblog_entry_richtextcontent',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
    ]
