from rest_framework import serializers

from gpstrack.tracks.models import Track, Point, Location, Time, Message


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['lat', 'lon', 'elevation']


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['UTC_time', 'local_time']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'location', 'time', 'text', 'active']


class PointSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    time = TimeSerializer()

    class Meta:
        model = Point
        fields = ['track', 'location', 'time', 'velocity', 'course', 'description', 'active', 'id']
        # ordering = ['-id']


class TrackSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Track
        fields = ['id', 'user', 'name', 'description', 'active', 'point_count', 'points', 'start_date', 'end_date']

    def get_points(selfset, obj):
        queryset = Point.objects.filter(track__id=obj.pk).prefetch_related()
        serializer = PointSerializer(queryset, many=True)
        return serializer.data
