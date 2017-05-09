from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from rest_framework import generics

from config.settings.base import GOOGLE_API_KEY
from gpstrack.tracks import permissions
from gpstrack.tracks.models import Track, Point
from gpstrack.tracks.serializer import TrackSerializer, PointSerializer


class MapView(TemplateView, ContextMixin):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_key'] = GOOGLE_API_KEY
        context['map_name'] = kwargs.get('map_name', 'eturner')
        return context


class TrackListView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def filter_queryset(self, queryset):
        filters = {
            'user__username': self.kwargs['map_name'],
            'active': True
        }
        if self.request.query_params.get('inactive', '') == 'true':
            filters.pop('active')
        return queryset.filter(**filters)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def filter_queryset(self, queryset):
        filters = {
            'user__username': self.kwargs['map_name']
        }
        return queryset.filter(**filters).order_by('-start_date')

class TrackPointList(generics.ListCreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def filter_queryset(self, queryset):
        filters = {
            'track__active': True,
            'track__user__username': self.kwargs['map_name'],
        }
        return queryset.filter(**filters)


class PointList(generics.ListCreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def filter_queryset(self, queryset):
        super().filter_queryset(queryset)
        filters = {
            'track__user__username': self.kwargs['map_name'],
        }
        if self.kwargs.get('track_pk'):
            filters['track'] = self.kwargs['track_pk']
        return queryset.filter(**filters)


class PointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def get_queryset(self):
        return super().get_queryset()
