from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect


class ForceDomainMiddleware(object):
    def __init__(self):
        if settings.DEBUG:
            raise MiddlewareNotUsed

        self.domain = getattr(settings, 'FORCE_DOMAIN', None)
        if not self.domain:
            raise MiddlewareNotUsed

    def process_request(self, request):
        if request.method != 'GET':
            return

        if request.META.get('HTTP_HOST') != self.domain:
            target = 'http%s://%s%s' % (
                request.is_secure() and 's' or '',
                self.domain,
                request.get_full_path())
            return HttpResponsePermanentRedirect(target)
