# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
# from feincms.content.application.models import ApplicationContent
# from feincms.content.raw.models import RawContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

# from elephantblog.contents import BlogEntryListContent
# from elephantblog.models import Entry

from feincms_cleanse import cleanse_html
from feincms_oembed.contents import OembedContent
# from form_designer.models import FormContent
#
# from .contents import (
#     SubpageContent, SlideContent, PageTeaserContent)


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
    'feincms.module.extensions.ct_tracker',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.titles',
    'feincms.module.page.extensions.navigationgroups',
)

# FeinCMS Contenttypes
# --------------------

Page.create_content_type(
    RichTextContent, cleanse=cleanse_html,
    optgroup='Content', regions=('main', 'col1', 'col2'))
Page.create_content_type(
    MediaFileContent,
    TYPE_CHOICES=(
        ('default', _('default')),
    ),
    optgroup='Content',
    regions=('main', 'col1', 'col2'))
Page.create_content_type(
    OembedContent,
    optgroup='Content',
    TYPE_CHOICES=[
        ('default', _('Default presentation'), {
            'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
    ])

# Page.create_content_type(
#     FormContent,
#     optgroup='Dynamic',
#     regions=('main', 'col1', 'col2'))
# Page.create_content_type(
#     SubpageContent,
#     optgroup='Content',
#     regions=('main', 'col1', 'col2'))
# Page.create_content_type(
#     PageTeaserContent,
#     optgroup='Content',
#     regions=('col1', 'col2'))
# Page.create_content_type(
#     BlogEntryListContent,
#     optgroup='Dynamic',
#     regions=('col1', 'col2'))
# Page.create_content_type(
#     ApplicationContent,
#     APPLICATIONS=(
#         ('elephantblog', _('Blog'), {
#             'urls': 'elephantblog.urls',
#         }),
#     ),
#     optgroup='Dynamic',
#     regions=('main', 'col1', 'col2'))
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
