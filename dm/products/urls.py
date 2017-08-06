from django.conf.urls import url
from products.views import (
                    ProductList,
                    ProductDetail,
                    ProductAdd,
                    ProductUpdate,
                    ProductDownload
)

urlpatterns = [

    url(r'^create/$', ProductAdd.as_view(),name='create'),
    url(r'^(?P<slug>[\w-]+)/detail/$',ProductDetail.as_view(),name='detail'),
    url(r'^(?P<slug>[\w-]+)/download/$',ProductDownload.as_view(),name='download'),
    url(r'^list/$', ProductList.as_view(),name='list'),
    url(r'^update/(?P<slug>[\w-]+)/$',ProductUpdate.as_view(),name='update'),

]
