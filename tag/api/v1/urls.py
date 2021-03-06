from django.conf.urls import url, include
from rest_framework import routers

from tag.api.v1 import views

router = routers.DefaultRouter()
router.register(r'tree-tags', views.ReadOnlyTreeTagViewSet)
router.register(r'tags', views.ReadOnlyTagViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]