from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.raw.models import RawContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.extensions import Extension
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile

from elephantblog.contents import BlogEntryListContent
from elephantblog.models import Entry

from feincms_cleanse import cleanse_html
from feincms_oembed.contents import OembedContent
from form_designer.models import FormContent

from {{ cookiecutter.project_name }}.cms.contents import (
    SubpageContent, SlideContent, PageTeaserContent)


Page.register_templates({
    'key': 'base',
    'title': _('Main area with sidebar'),
    'path': 'cms/standard.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('gallery', _('Gallery')),
    ),
}, {
    'key': 'full',
    'title': _('Full-width above, two columns below'),
    'path': 'cms/full_above.html',
    'regions': (
        ('main', _('Full width area')),
        ('col1', _('Left column')),
        ('col2', _('Right column')),
        ('gallery', _('Gallery')),
    ),
}, {
    'key': 'full_below',
    'title': _('Two columns above, full-width below'),
    'path': 'cms/full_below.html',
    'regions': (
        ('col1', _('Left column')),
        ('col2', _('Right column')),
        ('main', _('Full width area')),
        ('gallery', _('Gallery')),
    ),
})


class ExcerptExtension(Extension):
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


Page.register_extensions(
    'feincms.module.extensions.changedate',
    'feincms.module.extensions.ct_tracker',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.titles',
    'feincms.module.page.extensions.navigationgroups',
    ExcerptExtension,
)


Page.create_content_type(
    RichTextContent, cleanse=cleanse_html,
    optgroup='Content', regions=('main', 'col1', 'col2'))
Page.create_content_type(RawContent, optgroup='Content')
Page.create_content_type(SlideContent, regions=('gallery',))
Page.create_content_type(
    MediaFileContent,
    TYPE_CHOICES=(
        ('default', _('default')),
    ),
    optgroup='Content',
    regions=('main', 'col1', 'col2'))
Page.create_content_type(
    OembedContent,
    TYPE_CHOICES=[
        ('default', _('Default presentation'), {
            'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
    ])
Page.create_content_type(
    FormContent,
    optgroup='Dynamic',
    regions=('main', 'col1', 'col2'))
Page.create_content_type(
    SubpageContent,
    optgroup='Content',
    regions=('main', 'col1', 'col2'))
Page.create_content_type(
    PageTeaserContent,
    optgroup='Content',
    regions=('col1', 'col2'))
Page.create_content_type(
    BlogEntryListContent,
    optgroup='Dynamic',
    regions=('col1', 'col2'))
Page.create_content_type(
    ApplicationContent,
    APPLICATIONS=(
        ('elephantblog', _('Blog'), {
            'urls': 'elephantblog.urls',
        }),
    ),
    optgroup='Dynamic',
    regions=('main', 'col1', 'col2'))

Entry.register_regions(
    ('main', _('Main content area')),
)
Entry.create_content_type(RichTextContent, cleanse=cleanse_html)
Entry.create_content_type(
    MediaFileContent,
    TYPE_CHOICES=(
        ('default', _('default')),
    ))
Entry.create_content_type(
    OembedContent,
    TYPE_CHOICES=[
        ('default', _('Default presentation'), {
            'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
    ])
