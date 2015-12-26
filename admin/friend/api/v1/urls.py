from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter

from admin.friend.api.v1 import views

router = BulkRouter()
router.register(r'phone-contact-records', views.PhoneContactRecordViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]