from django.conf.urls import url, include
from rest_framework import routers
from friend.api.v1 import views

router = routers.DefaultRouter()
router.register(r'social-profiles', views.SocialProfileListView)


urlpatterns = [
    url('^has-friendship/$', views.has_friendship, name='friend_has_friendship'),
    url('^users/(?P<user_id>\d+)/tags/$', views.friend_tags, name='friend_tags_by_profile'),
    url('^alumni/$', views.alumni, name='friend_alumni'),
    url('^phone-contacts/$', views.phone_contacts, name='phone_contacts'),
    url('^phone-contacts/count/$', views.phone_contact_count, name='phone_contact_count'),
    url(r'^', include(router.urls)),
]