from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect


class ForceDomainMiddleware(object):
    def __init__(self):
        if settings.DEBUG:
            raise MiddlewareNotUsed

    def process_request(self, request):
        if request.method != 'GET':
            return

        domain = getattr(settings, 'FORCE_DOMAIN', None)

        if not domain:
            return

        if request.META['HTTP_HOST'] != domain:
            target = 'http%s://%s%s' % (
                request.is_secure() and 's' or '',
                domain,
                request.get_full_path())
            return HttpResponsePermanentRedirect(target)
