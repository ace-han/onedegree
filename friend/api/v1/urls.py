from django.conf.urls import patterns, url, include
from rest_framework import routers

from account.api.v1 import views

router = routers.DefaultRouter()
#router.register(r'friends', views.UserProfileViewSet)


urlpatterns = patterns('',
    url('^has-friendship/$', 'friend.api.v1.views.has_friendship', name='friend_has_friendship'),
    url(r'^', include(router.urls)),
)