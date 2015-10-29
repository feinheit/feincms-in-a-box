from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views import generic

from feincms.module.page.sitemap import PageSitemap

# from elephantblog.feeds import EntryFeed


admin.autodiscover()

sitemaps = {
    'pages': PageSitemap,
}

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^404/$', generic.TemplateView.as_view(template_name='404.html')),
    # url(r'^feeds/news/$', EntryFeed()),  # Elephantblog feed
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^rosetta/', include('rosetta.urls')),
]

if settings.DEBUG:
    try:
        urlpatterns += [
            url(r'^__debug__/', include(__import__('debug_toolbar').urls)),
        ]
    except ImportError:
        pass
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    ]

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    url(r'', include('feincms.contrib.preview.urls')),
    url(r'', include('feincms.urls')),
]
