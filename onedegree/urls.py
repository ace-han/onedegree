"""onedegree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from onedegree.views import index, admin_index

from django.views.i18n import javascript_catalog
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve as static_serve


# urlpatterns = i18n_patterns('', # will do i18n later in the future
urlpatterns = [
    #url(r'^auth/', include('authx.urls', namespace='auth')),
    #url(r'^authx/', include('authx.urls', namespace='authx')),
    url(r'^api/', include('onedegree.api.urls', namespace='api')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^sitemap\.xml$', sitemap),
    #url(r'^i18n/$', include('django.conf.urls.i18n')),
    url(r'^admin/$', admin_index, name='admin_index_page'),
    url(r'^$', index, name='index_page'),
    url(r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog),
]


if settings.DEBUG:
    urlpatterns = [
    url(r'^media/(?P<path>.*)$', static_serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + staticfiles_urlpatterns() + urlpatterns
