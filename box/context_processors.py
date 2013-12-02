from django.utils.functional import cached_property

from feincms.module.page.models import Page


class Context(object):
    def __init__(self, request):
        self.request = request

    @cached_property
    def meta_navigation(self):
        return Page.objects.in_navigation().filter(
            parent___cached_url='/meta/')


def box(request):
    return {
        'box': Context(request),
    }
