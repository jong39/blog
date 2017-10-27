from django.conf.urls import url
from django.contrib import admin

from . views import (
    post_list,
    post_detail,
    post_update,
)

urlpatterns = [
    url(r'^$', post_list),
    url(r'^create/$', "posts.views.post_create"),
    url(r'^(?P<id>\d+)/$', post_detail, name="mydetail"),
    url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
]