from __future__ import absolute_import, unicode_literals

from django import template


register = template.Library()


@register.filter
def group_by_tree(iterable):
    parent = None
    children = []
    level = -1

    for element in iterable:
        if parent is None or element.level == level:
            if parent:
                yield parent, children
                parent = None
                children = []

            parent = element
            level = element.level
        else:
            children.append(element)

    if parent:
        yield parent, children


@register.inclusion_tag('breadcrumbs.html')
def breadcrumbs(feincms_page, current=None):
    trail = [
        (
            page.get_navigation_url(),
            page.short_title(),
        )
        for page in feincms_page.get_ancestors(include_self=True).filter(
            in_navigation=True,
        )
    ]

    if current is not None:
        trail.append(('', current))

    return {
        'trail': trail,
    }
