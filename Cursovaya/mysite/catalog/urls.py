from django.conf.urls import url, include
from django.contrib import admin
from . import  views
from catalog.views import ProductListCat
from catalog.views import ProductDetail
from catalog.views import MainPage

urlpatterns = [

    url(r'main/', views.MainPage, name="main"),
     url(r'catalog/(?P<category_slug>[-\w]+)/$', views.ProductListCat, name="vitrina"),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='detail'),

        ]
