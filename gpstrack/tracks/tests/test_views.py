import json

from django.urls import reverse
from model_mommy import mommy
from test_plus.test import TestCase

from config.settings.base import GOOGLE_API_KEY


class UserMapViewTest(TestCase):
    def setUp(self):
        self.point = mommy.make('tracks.point')
        self.url = reverse('tracks:user_map', kwargs={'map_name': self.point.track.user.username})

    def test_MapView(self):
        response = self.client.get(self.url)
        assert 200 == response.status_code
        assert response.context_data['map_name'] == self.point.track.user.username
        assert response.context_data['api_key'] == GOOGLE_API_KEY


class TrackListTest(TestCase):
    def setUp(self):
        self.track = mommy.make('tracks.track')
        self.url = reverse('tracks:api.track_list', kwargs={'map_name': self.track.user.username})

    def test_track_list_get(self):
        response = self.client.get(self.url)
        assert 200 == response.status_code


class TrackDetailTest(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.track = mommy.make('tracks.track', user=self.user)
        self.url = reverse('tracks:api.track_detail',
                           kwargs={'map_name': self.user.username, 'pk': self.track.pk})

    def test_track_detail_get(self):
        response = self.client.get(self.url)
        assert 200 == response.status_code

    def test_track_detail_authorized_patch(self):
        self.client.login(username=self.user.username, password='password')
        request = self.client.patch(self.url, data=json.dumps({'name': 'Updated name'}),
                                    content_type='application/json')
        assert 200 == request.status_code

    def test_track_detail_authorized_delete(self):
        self.client.login(username=self.user.username, password='password')
        request = self.client.delete(self.url)
        assert 204 == request.status_code

    def test_track_detail_unauthorized_patch(self):
        request = self.client.patch(self.url, data=json.dumps({'name': 'Updated name'}),
                                    content_type='application/json')
        assert 403 == request.status_code

    def test_track_detail_unauthorized_delete(self):
        request = self.client.delete(self.url)
        assert 403 == request.status_code


class PointListTest(TestCase):
    def setUp(self):
        self.track = mommy.make('tracks.track')
        self.point = mommy.make('tracks.point', track=self.track)
        self.url = reverse('tracks:api.point_list',
                           kwargs={'map_name': self.track.user.username, 'track_pk': self.track.pk})

    def test_point_list_get(self):
        response = self.client.get(self.url)
        assert 200 == response.status_code


class PointDetailTest(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.track = mommy.make('tracks.track', user=self.user)
        self.point = mommy.make('tracks.point', track=self.track)
        self.url = reverse('tracks:api.point_detail',
                           kwargs={'map_name': self.user.username, 'pk': self.point.pk})

    def test_point_detail_get(self):
        response = self.client.get(self.url)
        assert 200 == response.status_code

    def test_point_detail_authorized_patch(self):
        self.client.login(username=self.user.username, password='password')
        request = self.client.patch(self.url, data=json.dumps({'description': 'Updated Desc'}),
                                    content_type='application/json')
        assert 200 == request.status_code

    def test_point_detail_authorized_delete(self):
        self.client.login(username=self.user.username, password='password')
        request = self.client.delete(self.url)
        assert 204 == request.status_code

    def test_point_detail_unauthorized_patch(self):
        request = self.client.patch(self.url, data=json.dumps({'description': 'Updated Desc'}),
                                    content_type='application/json')
        assert 403 == request.status_code

    def test_point_detail_unauthorized_delete(self):
        request = self.client.delete(self.url)
        assert 403 == request.status_code
