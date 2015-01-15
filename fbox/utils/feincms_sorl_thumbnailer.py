# coding: utf-8
"""
Thumbnailer class for FeinCMS.
Allows using sorl thumbnail as default thumbnailer.
Use this if you have mediafiles stored on S3.

Add this line to your settings:

    FEINCMS_MEDIALIBRARY_THUMBNAIL = 'feincms_sorl_thumbnailer.thumbnailer'

"""
from __future__ import unicode_literals
from sorl.thumbnail import get_thumbnail


def thumbnailer(mediafile, dimensions='100x100', quality=65, **kwargs):
    """
    Function called by FeinCMS medialibrary.thumbnail.admin_thumbnail
    :param mediafile: - the mediafile object
    :param kwargs: - options passed to the thumbnailer
    :return: - URL of the thumbnail
    """
    if mediafile.type == 'image':
        im = get_thumbnail(mediafile.file, dimensions, quality=quality)
        return im.url
    return ''
