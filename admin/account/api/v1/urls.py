from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter

from admin.account.api.v1 import views

router = BulkRouter()
router.register(r'schools', views.SchoolViewSet)
router.register(r'profiles', views.ProfileViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]