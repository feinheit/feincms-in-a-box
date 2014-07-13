# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.medialibrary.fields
import feincms.extensions
import feincms.module.mixins
import feincms.contrib.richtext
import feincms.contrib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('form_designer', '__first__'),
        ('elephantblog', '__first__'),
        ('medialibrary', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('parameters', feincms.contrib.fields.JSONField(editable=False, null=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('urlconf_path', models.CharField(max_length=100, verbose_name='application', choices=[('elephantblog', 'Blog')])),
            ],
            options={
                'db_table': 'page_page_applicationcontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'application content',
                'abstract': False,
                'verbose_name_plural': 'application contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogEntryListContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('paginate_by', models.PositiveIntegerField(verbose_name='entries per page', help_text='Set to 0 to disable pagination.', default=0)),
                ('featured_only', models.BooleanField(verbose_name='featured only', help_text='Only show articles marked as featured', default=False)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('category', models.ForeignKey(to='elephantblog.Category', help_text='Only show entries from this category.', null=True, blank=True, verbose_name='category')),
            ],
            options={
                'db_table': 'page_page_blogentrylistcontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'Blog entry list',
                'abstract': False,
                'verbose_name_plural': 'Blog entry lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('show_form_title', models.BooleanField(verbose_name='show form title', default=True)),
                ('success_message', models.TextField(verbose_name='success message', help_text='Custom message to display after valid form is submitted')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('form', models.ForeignKey(to='form_designer.Form', verbose_name='form')),
            ],
            options={
                'db_table': 'page_page_formcontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'form',
                'abstract': False,
                'verbose_name_plural': 'forms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaFileContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('type', models.CharField(max_length=20, verbose_name='type', default='default', choices=[('default', 'default')])),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile', verbose_name='media file')),
            ],
            options={
                'db_table': 'page_page_mediafilecontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'media file',
                'abstract': False,
                'verbose_name_plural': 'media files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('active', models.BooleanField(verbose_name='active', default=True)),
                ('title', models.CharField(max_length=200, verbose_name='title', help_text='This title is also used for navigation menu items.')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug', help_text='This is used to build the URL for this page')),
                ('in_navigation', models.BooleanField(verbose_name='in navigation', default=False)),
                ('override_url', models.CharField(blank=True, max_length=255, verbose_name='override URL', help_text="Override the target URL. Be sure to include slashes at the beginning and at the end if it is a local URL. This affects both the navigation and subpages' URLs.")),
                ('redirect_to', models.CharField(blank=True, max_length=255, verbose_name='redirect to', help_text='Target URL for automatic redirects or the primary key of a page.')),
                ('_cached_url', models.CharField(max_length=255, default='', blank=True, verbose_name='Cached URL', editable=False, db_index=True)),
                ('template_key', models.CharField(max_length=255, verbose_name='template', default='base', choices=[('base', 'Main area with sidebar'), ('full', 'Full-width above, two columns below'), ('full_below', 'Two columns above, full-width below')])),
                ('creation_date', models.DateTimeField(verbose_name='creation date', null=True, editable=False)),
                ('modification_date', models.DateTimeField(verbose_name='modification date', null=True, editable=False)),
                ('_ct_inventory', feincms.contrib.fields.JSONField(blank=True, verbose_name='content types', null=True, editable=False)),
                ('navigation_extension', models.CharField(blank=True, max_length=200, verbose_name='navigation extension', null=True, help_text='Select the module providing subpages for this page if you need to customize the navigation.')),
                ('meta_keywords', models.TextField(blank=True, verbose_name='meta keywords', help_text='Keywords are ignored by most search engines.')),
                ('meta_description', models.TextField(blank=True, verbose_name='meta description', help_text='This text is displayed on the search results page. It is however not used for the SEO ranking. Text longer than 140 characters is truncated.')),
                ('_content_title', models.TextField(blank=True, verbose_name='content title', help_text='The first line is the main title, the following lines are subtitles.')),
                ('_page_title', models.CharField(blank=True, max_length=69, verbose_name='page title', help_text='Page title for browser window. Same as title bydefault. Must not be longer than 70 characters.')),
                ('excerpt_text', models.TextField(blank=True, verbose_name='text')),
                ('excerpt_image', feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile', null=True, blank=True, verbose_name='image')),
                ('parent', models.ForeignKey(to='page.Page', null=True, blank=True, verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'page',
                'ordering': ['tree_id', 'lft'],
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
        migrations.AddField(
            model_name='mediafilecontent',
            name='parent',
            field=models.ForeignKey(to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formcontent',
            name='parent',
            field=models.ForeignKey(to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogentrylistcontent',
            name='parent',
            field=models.ForeignKey(to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicationcontent',
            name='parent',
            field=models.ForeignKey(to='page.Page'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='PageTeaserContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile', verbose_name='mediafile')),
                ('page', models.ForeignKey(to='page.Page', verbose_name='page')),
                ('parent', models.ForeignKey(to='page.Page')),
            ],
            options={
                'db_table': 'page_page_pageteasercontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'page teaser',
                'abstract': False,
                'verbose_name_plural': 'page teasers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('text', models.TextField(blank=True, verbose_name='content')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('parent', models.ForeignKey(to='page.Page')),
            ],
            options={
                'db_table': 'page_page_rawcontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'raw content',
                'abstract': False,
                'verbose_name_plural': 'raw contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('text', feincms.contrib.richtext.RichTextField(blank=True, verbose_name='text')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('parent', models.ForeignKey(to='page.Page')),
            ],
            options={
                'db_table': 'page_page_richtextcontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'rich text',
                'abstract': False,
                'verbose_name_plural': 'rich texts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlideContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('subtitle', models.CharField(blank=True, max_length=100, verbose_name='subtitle')),
                ('area', models.CharField(max_length=10, verbose_name='preferred area if cropping', default='50x50', choices=[('50x50', 'center'), ('50x20', 'center / top'), ('20x50', 'left / center'), ('80x50', 'right / center'), ('50x80', 'center / bottom')])),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile', verbose_name='media file')),
                ('parent', models.ForeignKey(to='page.Page')),
            ],
            options={
                'db_table': 'page_page_slidecontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'slide',
                'abstract': False,
                'verbose_name_plural': 'slides',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubpageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('style', models.CharField(max_length=20, verbose_name='style', default='default', choices=[('default', 'list'), ('grid', 'grid')])),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('parent', models.ForeignKey(to='page.Page')),
            ],
            options={
                'db_table': 'page_page_subpagecontent',
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'subpages listing',
                'abstract': False,
                'verbose_name_plural': 'subpages listings',
            },
            bases=(models.Model,),
        ),
    ]
