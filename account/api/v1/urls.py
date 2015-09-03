from django.conf.urls import patterns, url, include
from rest_framework import routers

from account.api.v1 import views

router = routers.DefaultRouter()
router.register(r'schools', views.SchoolViewSet)
router.register(r'profiles', views.ProfileViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)