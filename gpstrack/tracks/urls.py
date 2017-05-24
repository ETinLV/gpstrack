# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #-----Page URLs-----
    url(r'^$',views.MapView.as_view(),name='home'),
    url(r'^(?P<map_name>[\w.@+-]+)/$', views.MapView.as_view(), name='user_map'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),


    #-----API URLs-----

    # Tracks
    url(r'^api/(?P<map_name>[\w.@+-]+)/tracks/$', views.TrackListView.as_view(), name='api.track_list'),
    url(r'^api/(?P<map_name>[\w.@+-]+)/tracks/(?P<pk>[0-9]+)/$', views.TrackDetail.as_view(), name='api.track_detail'),

    # Points
    url(r'^api/(?P<map_name>[\w.@+-]+)/tracks/(?P<track_pk>[0-9]+)/points/$', views.PointList.as_view(),
        name='api.point_list'),
    url(r'^api/(?P<map_name>[\w.@+-]+)/points/(?P<pk>[0-9]+)/$', views.PointDetail.as_view(), name='api.point_detail'),

]
