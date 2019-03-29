from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^remove/(?P<tour_id>\d+)/$', views.CartRemove, name='CartRemove'),
    url(r'^add/(?P<tour_id>\d+)/$', views.CartAdd, name='CartAdd'),
    url(r'^$', views.CartDetail, name='CartDetail'),
]