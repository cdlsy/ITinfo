from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url
from job.views import IndexView
app_name='job'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
