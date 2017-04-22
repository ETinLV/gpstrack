from django.db import models

from django.conf import settings




class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)

class Point(models.Model):
    track = models.ForeignKey(to=Track, null=True)
    location = models.ForeignKey(to='Location')
    time = models.ForeignKey(to='Time')
    velocity = models.FloatField(blank=True)
    course = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    location = models.ForeignKey(to='Location')
    time = models.ForeignKey(to='Time')
    text = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)

class Time(models.Model):
    UTC_time = models.DateTimeField()
    local_time = models.DateTimeField()

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
