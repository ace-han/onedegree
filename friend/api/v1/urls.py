from django.conf.urls import patterns, url, include
from rest_framework import routers


router = routers.DefaultRouter()
#router.register(r'friends', views.UserProfileViewSet)


urlpatterns = patterns('',
    url('^has-friendship/$', 'friend.api.v1.views.has_friendship', name='friend_has_friendship'),
    url('^users/(?P<user_id>\d+)/tags/$', 'friend.api.v1.views.friend_tags', name='friend_tags_by_profile'),
    url(r'^', include(router.urls)),
)