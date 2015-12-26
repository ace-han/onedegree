from django.conf.urls import url, include

import admin.tag.api.v1.urls as admin_tag_urls
import admin.auth.api.v1.urls as admin_auth_urls
import admin.account.api.v1.urls as admin_account_urls
import admin.friend.api.v1.urls as admin_friend_urls

urlpatterns = [
    url(r'^tag/', include(admin_tag_urls, namespace='tag')),
    url(r'^auth/', include(admin_auth_urls, namespace='auth')),
    url(r'^account/', include(admin_account_urls, namespace='account')),
    url(r'^friend/', include(admin_friend_urls, namespace='friend')),
]