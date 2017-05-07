from django.conf import settings
from django.db import models
from timezone_field import TimeZoneField


class TrackManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('points', )


class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = TrackManager()

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def start_date(self):
        if self.points.exists():
            return self.points.first().time.UTC_time
        return None

    @property
    def end_date(self):
        if self.points.exists():
            return self.points.last().time.UTC_time
        return None

    @property
    def point_count(self):
        return self.points.count()

    @property
    def duration(self):
        if self.points.exists():
            return self.end_date - self.start_date
        return None


class PointManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('time', 'location')


class Point(models.Model):
    track = models.ForeignKey(to=Track, null=True, related_name='points')
    location = models.ForeignKey(to='Location', related_name='points')
    time = models.OneToOneField(to='Time', db_index=True, related_name='points')
    velocity = models.FloatField(blank=True)
    course = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = PointManager()

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        ordering = ['time__UTC_time']


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('time', 'location')


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages')
    location = models.ForeignKey(to='Location', related_name='location')
    time = models.OneToOneField(to='Time', related_name='time')
    text = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = MessageManager()

    def __str__(self):
        return '{} | {}'.format(self.user, self.time)


class Time(models.Model):
    UTC_time = models.DateTimeField(db_index=True)
    local_time = models.DateTimeField(null=True, blank=True)
    local_time_zone = TimeZoneField()

    def __str__(self):
        return '{} | {}'.format(self.UTC_time.date(), self.local_time.time())


class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)
