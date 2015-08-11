from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^(?P<version>v1)/', include('onedegree.api.v1.urls', namespace='v1')),
)