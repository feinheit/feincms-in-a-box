from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.admin.item_editor import FeinCMSInline
from feincms.content.medialibrary.models import MediaFileContent
from feincms.module.medialibrary.fields import (
    ContentWithMediaFile, MediaFileForeignKey)
from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.models import Page


class SubpageContent(models.Model):
    style = models.CharField(
        _('style'),
        max_length=20,
        choices=(
            ('default', _('list')),
            ('grid', _('grid')),
        ),
        default='default')

    class Meta:
        abstract = True
        verbose_name = _('subpages listing')
        verbose_name_plural = _('subpages listings')

    def render(self, **kwargs):
        return render_to_string([
            'content/subpage/%s.html' % self.style,
            'content/subpage/default.html',
        ], {
            'content': self,
            'page_list': self.parent.children.in_navigation().select_related(
                'excerpt_image'),
        })


class SlideContent(ContentWithMediaFile):
    title = models.CharField(_('title'), max_length=100, blank=True)
    subtitle = models.CharField(_('subtitle'), max_length=100, blank=True)
    area = models.CharField(
        _('preferred area if cropping'),
        max_length=10,
        choices=(
            ('50x50', _('center')),
            ('50x20', _('center / top')),
            ('20x50', _('left / center')),
            ('80x50', _('right / center')),
            ('50x80', _('center / bottom')),
        ),
        default='50x50')

    class Meta:
        abstract = True
        verbose_name = _('slide')
        verbose_name_plural = _('slides')

    def render(self, **kwargs):
        return render_to_string([
            'content/slide/default.html',
        ], {'content': self})

    @property
    def crop(self):
        return '950x360-%s' % self.area


class PageTeaserInline(FeinCMSInline):
    raw_id_fields = ('page', 'mediafile')


class PageTeaserContent(models.Model):
    feincms_item_editor_inline = PageTeaserInline

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='+')
    mediafile = MediaFileForeignKey(
        MediaFile, verbose_name=_('mediafile'), related_name='+')
    title = models.CharField(_('title'), max_length=100, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('page teaser')
        verbose_name_plural = _('page teasers')

    @classmethod
    def get_queryset(cls, filter_args):
        return cls.objects.filter(filter_args).select_related(
            'parent', 'page', 'mediafile')

    def render(self, **kwargs):
        return render_to_string('content/pageteaser/default.html', {
            'content': self,
        })

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.page.title
        if not self.mediafile:
            try:
                self.mediafile = self.page.content.all_of_type(
                    MediaFileContent)[0]
            except IndexError:
                pass
        super(PageTeaserContent, self).save(*args, **kwargs)
