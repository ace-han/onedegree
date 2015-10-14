from django.conf.urls import patterns, url, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = patterns('authx.api.v1.views',
    #url(r'^', include(router.urls)),
    url(r'^token/$', 'obtain_jwt_token'),
    url(r'^token/refresh/$', 'refresh_jwt_token'),
    url(r'^token/verify/$', 'verify_jwt_token'),
    url(r'^register/$', 'register'),
    url(r'^login/$', 'login'),
)
