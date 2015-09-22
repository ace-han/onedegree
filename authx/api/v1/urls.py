from django.conf.urls import patterns, url, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = patterns('',
    #url(r'^', include(router.urls)),
    url(r'^login/$', obtain_jwt_token),
)
