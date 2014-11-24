# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_oembedcontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='navigation_group',
            field=models.CharField(default='default', max_length=20, verbose_name='navigation group', db_index=True, choices=[('default', 'Default'), ('footer', 'Footer')]),
            preserve_default=True,
        ),
    ]
