from django.conf.urls import url, include
from rest_framework import routers

from authx.api.v1 import views


router = routers.DefaultRouter()
router.register('users', views.UserRetrieveUpdateViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token/$', views.obtain_jwt_token),
    url(r'^token/refresh/$', views.refresh_jwt_token),
    url(r'^token/verify/$', views.verify_jwt_token),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
]
