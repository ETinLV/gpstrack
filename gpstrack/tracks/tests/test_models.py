from model_mommy import mommy
from test_plus.test import TestCase

from gpstrack.tracks.models import Time


class TestTrack(TestCase):
    def setUp(self):
        self.user = mommy.make('users.user')
        self.track = mommy.make('tracks.track', user=self.user)
        self.point1 = mommy.make('tracks.point', track=self.track)
        self.point2 = mommy.make('tracks.point', track=self.track)

    def test__str__(self):
        self.assertEqual(
            self.track.__str__(),
            '1'
        )

    def test_get_owner(self):
        assert self.track.get_owner() == self.user

    def test_point_count(self):
        assert self.track.point_count == 2

    def test_start_date(self):
        assert self.track.start_date == min(
            Time.objects.filter(point__in=[self.point1, self.point2]).values_list('UTC_time', flat=True))

        # def test_end_date(self):
        #     assert self.track.end_date > self.track.start_date


        # TestTrack.setUp()
        # TestTrack.test_start_date()
