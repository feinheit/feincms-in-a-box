# coding: utf-8
"""
Thumbnailer class for FeinCMS.
Allows using easythumbnail as default thumbnailer.

Add this line to your settings:

    FEINCMS_MEDIALIBRARY_THUMBNAIL = 'feincms_easy_thumbnailer.thumbnailer'

"""
from __future__ import unicode_literals
import re
from easy_thumbnails.files import get_thumbnailer

RE_SIZE = re.compile(r'(\d+)x(\d+)$')


def thumbnailer(mediafile, dimensions='100x100', quality=85, **kwargs):
    """
    Function called by FeinCMS medialibrary.thumbnail.admin_thumbnail
    :param mediafile: - the mediafile object
    :param kwargs: - options passed to the thumbnailer
    :return: - URL of the thumbnail
    """
    m = RE_SIZE.match(dimensions)
    if m:
        kwargs['size'] = (int(m.group(1)), int(m.group(2)))
    kwargs['quality'] = quality

    if mediafile.type == 'image':
        return get_thumbnailer(mediafile.file).get_thumbnail(kwargs).url
    return ''
