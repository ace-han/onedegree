from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^tag/', include('tag.api.v1.urls', namespace='tag')),
    url(r'^admin/', include('admin.api.v1.urls', namespace='admin')),
)