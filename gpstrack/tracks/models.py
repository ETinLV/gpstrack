from django.conf import settings
from django.db import models


class TrackManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('points', )

class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = TrackManager()

    @property
    def start_date(self):
        return self.points.first().time.UTC_time

    @property
    def end_date(self):
        return self.points.last().time.UTC_time

    @property
    def point_count(self):
        return self.points.count()


class PointManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('time', 'location')


class Point(models.Model):
    track = models.ForeignKey(to=Track, null=True, related_name='points')
    location = models.ForeignKey(to='Location', related_name='points')
    time = models.ForeignKey(to='Time', db_index=True, related_name='points')
    velocity = models.FloatField(blank=True)
    course = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = PointManager()

    class Meta:
        ordering = ['time__UTC_time']


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('time', 'location')


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages')
    location = models.ForeignKey(to='Location', related_name='location')
    time = models.ForeignKey(to='Time', related_name='time')
    text = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = MessageManager()


class Time(models.Model):
    UTC_time = models.DateTimeField(db_index=True)
    local_time = models.DateTimeField()


class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
