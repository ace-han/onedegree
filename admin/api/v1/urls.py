from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^tag/', include('admin.tag.api.v1.urls', namespace='tag')),
    url(r'^auth/', include('admin.auth.api.v1.urls', namespace='auth')),
)