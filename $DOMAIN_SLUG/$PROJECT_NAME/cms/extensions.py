# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.extensions import Extension
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile

class ExcerptExtension(Extension):
    """
    TODO: A description describing what this extension is doing.
    """
    def handle_model(self):
        self.model.add_to_class(
            'excerpt_image',
            MediaFileForeignKey(
                MediaFile, verbose_name=_('image'),
                blank=True, null=True, related_name='+'))
        self.model.add_to_class(
            'excerpt_text',
            models.TextField(_('text'), blank=True))

    def handle_modeladmin(self, modeladmin):
        modeladmin.raw_id_fields.append('excerpt_image')
        modeladmin.add_extension_options(_('Excerpt'), {
            'fields': ('excerpt_image', 'excerpt_text'),
        })

