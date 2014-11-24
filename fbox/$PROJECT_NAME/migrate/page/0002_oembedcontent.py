# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OembedContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text='Insert an URL to an external content you want to embed, e.g. http://www.youtube.com/watch?v=Nd-vBFJN_2E', verbose_name='URL')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('type', models.CharField(default='default', max_length=20, verbose_name='type', choices=[('default', 'Default presentation')])),
                ('parent', models.ForeignKey(to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'external contents',
                'db_table': 'page_page_oembedcontent',
                'verbose_name': 'external content',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
    ]
