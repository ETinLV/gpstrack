import json

from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import GOOGLE_API_KEY
from gpstrack.tracks.models import Track, Point
from gpstrack.tracks.serializer import TrackSerializer, PointSerializer


class MapView(TemplateView, ContextMixin):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_key'] = GOOGLE_API_KEY
        return context


class TrackListView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def filter_queryset(self, queryset):
        filters = {}
        if self.kwargs.get('all'):
            filters['active'] = True
        return queryset.filter(**filters)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackPointList(generics.ListCreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def filter_queryset(self, queryset):
        filters = {}
        if self.kwargs.get('track_pk'):
            filters['track'] = self.kwargs['track_pk']
        return queryset.filter(**filters)


class PointListView(generics.ListCreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class PointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
