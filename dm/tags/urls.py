from django.conf.urls import url
from tags.views import (
                    TagDetailView,
                    TagListView
)

urlpatterns = [


    url(r'^(?P<slug>[\w-]+)/detail/$',TagDetailView.as_view(),name='detail'),

    url(r'^list/$', TagListView.as_view(),name='list'),


]
