# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import feincms.translations
import feincms.extensions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('slug', models.SlugField(verbose_name='slug', max_length=150)),
                ('parent', models.ForeignKey(null=True, verbose_name='parent', blank=True, to='medialibrary.Category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['parent__title', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file', models.FileField(verbose_name='file', max_length=255, upload_to='medialibrary/%Y/%m/')),
                ('type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('pdf', 'PDF document'), ('swf', 'Flash'), ('txt', 'Text'), ('rtf', 'Rich Text'), ('zip', 'Zip archive'), ('doc', 'Microsoft Word'), ('xls', 'Microsoft Excel'), ('ppt', 'Microsoft PowerPoint'), ('other', 'Binary')], verbose_name='file type', max_length=12, editable=False)),
                ('created', models.DateTimeField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('copyright', models.CharField(verbose_name='copyright', blank=True, max_length=200)),
                ('file_size', models.IntegerField(verbose_name='file size', null=True, blank=True, editable=False)),
                ('categories', models.ManyToManyField(verbose_name='categories', null=True, blank=True, to='medialibrary.Category')),
            ],
            options={
                'verbose_name': 'media file',
                'verbose_name_plural': 'media files',
                'abstract': False,
                'ordering': ['-created'],
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='MediaFileTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('language_code', models.CharField(choices=[('de', 'German')], verbose_name='language', max_length=10, default='de', editable=False)),
                ('caption', models.CharField(verbose_name='caption', max_length=200)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('parent', models.ForeignKey(to='medialibrary.MediaFile')),
            ],
            options={
                'verbose_name': 'media file translation',
                'verbose_name_plural': 'media file translations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='mediafiletranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
    ]
