from __future__ import absolute_import, unicode_literals

from django.utils.functional import cached_property

from feincms.module.page.models import Page


class Context(object):
    def __init__(self, request):
        self.request = request

    @cached_property
    def meta_navigation(self):
        return Page.objects.in_navigation().filter(
            parent___cached_url='/meta/')


def {{ cookiecutter.project_name }}_context(request):
    return {
        '{{ cookiecutter.project_name }}': Context(request),
    }
