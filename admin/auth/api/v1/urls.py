from django.conf.urls import patterns, url, include
from rest_framework_bulk.routes import BulkRouter

from admin.auth.api.v1 import views

router = BulkRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)