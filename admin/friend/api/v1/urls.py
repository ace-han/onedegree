from django.conf.urls import patterns, url, include
from rest_framework_bulk.routes import BulkRouter

from admin.friend.api.v1 import views

router = BulkRouter()
router.register(r'contact-records', views.ContactRecordViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)