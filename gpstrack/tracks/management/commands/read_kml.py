import re

import pytz
import xmltodict
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.datetime_safe import datetime
from tzwhere import tzwhere

from gpstrack.tracks.models import Track, Point, Time, Location, Message
from gpstrack.users.models import User

BASE_DIR = settings.BASE_DIR
# this takes ~20 seconds to init, so init only once on run
TZ = tzwhere.tzwhere()


# On production use this instead: long INIT, but faster performance
# TZ = tzwhere.tzwhere(shapely=True)


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        self.parse_xml()

    def parse_xml(self):

        xml_file = settings.ROOT_DIR + 'tracks.kml'
        with open(xml_file.root, "rb") as f:
            d = xmltodict.parse(f, xml_attribs=True)
        objs_created = {
            'tracks': 0,
            'points': 0,
            'messages': 0,
            'times': 0,
            'locations': 0
        }
        for route in d['kml']['Document']['Folder']:
            user = User.objects.get(id=1)
            track, tr_created = Track.objects.update_or_create(
                user=user,
                name='{} {} - {}'.format(route['name'],
                                         convert_route_time(route['Placemark'][0]['TimeStamp']['when']).date(),
                                         convert_route_time(route['Placemark'][-2]['TimeStamp']['when']).date()),
                description='My Track')
            if tr_created:
                objs_created['tracks'] += 1
            for point in route['Placemark']:
                try:
                    data = point['ExtendedData']['Data']
                    if not data[15]['value']:
                        time, t_created = Time.objects.update_or_create(
                            UTC_time=convert_point_time(data[1]['value']))
                        location, l_created = Location.objects.update_or_create(
                            lat=data[8]['value'],
                            lon=data[9]['value'],
                            elevation=convert_elevation(data[10]['value']))

                        point, p_created = Point.objects.update_or_create(
                            track=track,
                            time=time,
                            location=location,
                            velocity=convert_velocity(data[11]['value']),
                            course=convert_course(data[12]['value']),
                        )
                        covert_utc_to_location(point)
                        if t_created:
                            objs_created['times'] += 1
                        if l_created:
                            objs_created['locations'] += 1
                        if p_created:
                            objs_created['points'] += 1
                    else:
                        time, t_created = Time.objects.update_or_create(
                            UTC_time=convert_point_time(data[1]['value']))
                        location, l_created = Location.objects.update_or_create(
                            lat=data[8]['value'],
                            lon=data[9]['value'],
                            elevation=convert_elevation(data[10]['value']))

                        message, m_created = Message.objects.update_or_create(
                            user=user,
                            time=time,
                            location=location,
                            text=data[15]['value'],
                        )
                        covert_utc_to_location(message)
                        if m_created:
                            objs_created['messages'] += 1
                        if t_created:
                            objs_created['times'] += 1
                        if l_created:
                            objs_created['locations'] += 1
                except KeyError:
                    pass
        print('\033[92mCreated\n{} Tracks\n{} Points\n{} Messages\n{} Times\n{} Locations'.format(
            objs_created['tracks'],
            objs_created['points'],
            objs_created['messages'],
            objs_created['times'],
            objs_created['locations']))


def convert_route_time(time):
    return timezone.make_aware(datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'), timezone=pytz.UTC)


def convert_point_time(time):
    """Point in UTC, this is not ISO format"""
    return timezone.make_aware(datetime.strptime(time, '%m/%d/%Y %I:%M:%S %p'),
                               timezone=pytz.UTC)


def covert_utc_to_location(obj):
    timezone_str = TZ.tzNameAt(float(obj.location.lat), float(obj.location.lon))
    local_time_zone = pytz.timezone(timezone_str)
    obj.time.local_time = timezone.make_naive(obj.time.UTC_time, local_time_zone)
    obj.time.local_time_zone = local_time_zone
    obj.time.save()


def convert_elevation(elevation):
    """convert elevation in meters to FT"""
    meters = re.match('[0-9.]*', elevation)[0]
    meters = float(meters)
    return round(meters * 3.280831, 4)


def convert_velocity(velocity):
    """convert Kilometers/h to Miles/h"""
    velocity = re.match('[0-9.]*', velocity)[0]
    velocity = float(velocity)
    return round(velocity * 0.621371, 4)


def convert_course(course):
    if course:
        course = re.match('[0-9.]*', course)[0]
        return course
    return
