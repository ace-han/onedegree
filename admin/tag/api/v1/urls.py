from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter

from admin.tag.api.v1 import views

router = BulkRouter()
router.register(r'tree-tags', views.TreeTagViewSet)
router.register(r'tags', views.TagViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]