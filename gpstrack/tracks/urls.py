# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #-----Page URLs-----
    url(r'^$',views.MapView.as_view(),name='home'),
    url(r'^about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),


    #-----API URLs-----

    # Tracks
    url(r'^api/tracks/$', views.TrackListView.as_view(), name='api.track_list'),
    url(r'^api/tracks/(?P<pk>[0-9]+)/$', views.TrackDetail.as_view(), name='api.track_detail'),
    url(r'^api/tracks/(?P<track_pk>[0-9]+)/points/$', views.PointList.as_view(), name='api.track_point_list_detail'),

    # Points
    url(r'^api/points/$', views.TrackPointList.as_view(), name='api.point_list'),
    url(r'^api/points/$', views.PointList.as_view(), name='api.point_list'),
    url(r'^api/points/(?P<pk>[0-9]+)/$', views.PointDetail.as_view(), name='api.point_detail'),

]
