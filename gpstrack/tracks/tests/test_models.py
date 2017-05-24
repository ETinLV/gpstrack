from datetime import timedelta

from django.utils.datetime_safe import datetime
from model_mommy import mommy
from test_plus.test import TestCase

from gpstrack.tracks.models import Track


class TestTrackManager(TestCase):
    def setUp(self):
        self.track = mommy.make('tracks.track')

    def test_all(self):
        assert list(Track.objects.all()) == [self.track]


class TestTrack(TestCase):
    def setUp(self):
        self.user = mommy.make('users.user')
        self.track = mommy.make('tracks.track', user=self.user)
        # First point
        self.point1 = mommy.make('tracks.point', track=self.track, time__UTC_time=datetime.now() - timedelta(days=7))
        # Middle point
        self.point2 = mommy.make('tracks.point', track=self.track, time__UTC_time=datetime.now() - timedelta(days=1))
        # Last point
        self.point3 = mommy.make('tracks.point', track=self.track, time__UTC_time=datetime.now() - timedelta(hours=1))

    def test__str__(self):
        assert self.track.__str__() == str(self.track.id)

    def test_get_owner(self):
        assert self.track.get_owner() == self.user

    def test_point_count(self):
        assert self.track.point_count == 3

    def test_start_date(self):
        assert self.track.start_date == self.point1.time.UTC_time

    def test_end_date(self):
        assert self.track.end_date == self.point3.time.UTC_time

    def test_duration(self):
        assert self.track.duration == (self.point3.time.UTC_time - self.point1.time.UTC_time)
