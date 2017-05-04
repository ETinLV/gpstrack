from django.contrib import admin

# Register your models here.
from gpstrack.tracks import models

app_models = []

admin.site.register(app_models)


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'description', 'start_date', 'end_date', 'point_count', 'duration', 'active')


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'track', 'time', 'active',)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'time', 'text', 'active',)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'lon')


@admin.register(models.Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'UTC_time', 'local_time')
