from django.conf.urls import url, include
from rest_framework import routers

from account.api.v1 import views

router = routers.DefaultRouter()
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'schools', views.SchoolViewSet)


urlpatterns = [
    url('^cities/$', views.city_list, name='account_city_list'),
    url('^genders/$', views.gender_list, name='account_gender_list'),
    url(r'^', include(router.urls)),
]