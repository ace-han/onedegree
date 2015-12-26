from django.conf.urls import url, include
from onedegree.api.v1 import urls as onedegree_api_urls

urlpatterns = [
    url(r'^(?P<version>v1)/', include(onedegree_api_urls, namespace='v1')),
]