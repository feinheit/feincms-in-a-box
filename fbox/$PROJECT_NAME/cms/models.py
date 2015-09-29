# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

# from feincms.apps import ApplicationContent
from feincms.contents import (
    RichTextContent,
    FilerImageContent,
    FilerFileContent,
)
from feincms.module.page.models import Page

# from elephantblog.contents import BlogEntryListContent
# from elephantblog.models import Entry

from feincms_cleanse import cleanse_html
from feincms_oembed.contents import OembedContent
from form_designer.models import FormContent


Page.register_templates({
    'key': 'base',
    'title': _('Main area with sidebar'),
    'path': 'cms/standard.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
    ),
},
)


Page.register_extensions(
    'feincms.extensions.ct_tracker',
    'feincms.extensions.seo',
    'feincms.module.page.extensions.titles',
    'feincms.module.page.extensions.navigationgroups',
    'feincms.extensions.translations',
)

# FeinCMS Contenttypes
# --------------------

Page.create_content_type(
    RichTextContent, cleanse=cleanse_html,
)
Page.create_content_type(
    FilerImageContent,
    TYPE_CHOICES=(
        ('block', _('Full width')),
    ),
)
Page.create_content_type(
    FilerFileContent,
)
Page.create_content_type(
    OembedContent,
    TYPE_CHOICES=[
        ('default', _('Default presentation'), {
            'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
    ],
)

Page.create_content_type(
    FormContent)

# Page.create_content_type(
#     SubpageContent)
# Page.create_content_type(
#     PageTeaserContent)
# Page.create_content_type(
#     BlogEntryListContent)
# Page.create_content_type(
#     ApplicationContent,
#     APPLICATIONS=(
#         ('elephantblog', _('Blog'), {
#             'urls': 'elephantblog.urls',
#         }),
#     ))
#

# Elephantblog Contenttypes
# -------------------------

# Entry.register_regions(
#     ('main', _('Main content area')),
# )
# Entry.create_content_type(RichTextContent, cleanse=cleanse_html)
# Entry.create_content_type(
#     MediaFileContent,
#     TYPE_CHOICES=(
#         ('default', _('default')),
#     ))
# Entry.create_content_type(
#     OembedContent,
#     TYPE_CHOICES=[
#         ('default', _('Default presentation'), {
#             'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
#     ])
