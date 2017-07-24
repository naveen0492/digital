"""dm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from products import views
from products.views import (
                    ProductList,
                    ProductDetail,
                    ProductAdd,
                    ProductUpdate
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create/', ProductAdd.as_view(),name='create'),
    url(r'^detail/(?P<object_id>\d+)/$',views.detail_view,name='detail'),
    url(r'^detail/(?P<slug>[\w-]+)/$',views.ProductDetail.as_view(),name='detail_slug_view'),
    url(r'^detail/(?P<slug>[\w-]+)/$',views.detail_slug_view,name='detail_slug_view'),
    url(r'^list/$', ProductList.as_view(),name='list'),
    url(r'^update/(?P<slug>[\w-]+)/$',ProductUpdate.as_view(),name='update'),

]
