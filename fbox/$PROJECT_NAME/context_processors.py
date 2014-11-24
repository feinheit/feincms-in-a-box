from __future__ import absolute_import, unicode_literals

# from django.utils.functional import cached_property
# from feincms.module.page.models import Page


class Context(object):
    def __init__(self, request):
        self.request = request

    # @cached_property
    # def some_useful_context_variable():
    #     return ...


def site_context(request):
    return {
        '${PROJECT_NAME}': Context(request),
    }
