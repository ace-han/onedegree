from django.conf.urls import url, include

import tag.api.v1.urls as tag_urls
import admin.api.v1.urls as admin_urls
import authx.api.v1.urls as authx_urls
import account.api.v1.urls as account_urls
import friend.api.v1.urls as friend_urls

urlpatterns = [
    url(r'^tag/', include(tag_urls, namespace='tag')),
    url(r'^admin/', include(admin_urls, namespace='admin')),
    url(r'^authx/', include(authx_urls, namespace='authx')), # just to align the naming pattern
    url(r'^auth/', include(authx_urls, namespace='auth')), # use this default
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^friend/', include(friend_urls, namespace='friend')),
]