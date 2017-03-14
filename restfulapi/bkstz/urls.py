from django.conf.urls import url
from django.contrib import admin
from views import get_bkstz
urlpatterns = [
    url(r'^$', get_bkstz),
    url(r'^([a-f\d]{24})/$', get_bkstz),
]
