from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^tag/', include('tag.api.v1.urls', namespace='tag')),
    url(r'^admin/', include('admin.api.v1.urls', namespace='admin')),
    url(r'^authx/', include('authx.api.v1.urls', namespace='authx')), # just to align the naming pattern
    url(r'^auth/', include('authx.api.v1.urls', namespace='auth')), # use this default
    url(r'^account/', include('account.api.v1.urls', namespace='account')),
    url(r'^friend/', include('friend.api.v1.urls', namespace='friend')),
)