import re

import pytz
import xmltodict
from django.utils import timezone
from django.utils.datetime_safe import datetime

from gpstrack.tracks.models import Track, Point, Time, Location, Message

from django.conf import settings
from django.core.management.base import BaseCommand

from gpstrack.users.models import User

BASE_DIR = settings.BASE_DIR
"""This did not work so well, revist later"""

class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        self.parse_xml()

    def parse_xml(self):

        xml_file = settings.ROOT_DIR + 'tracks.kml'
        with open(xml_file.root, "rb") as f:
            d = xmltodict.parse(f, xml_attribs=True)
        routes, points, messages = 0,0,0
        for route in d['kml']['Document']['Folder']:
            user = User.objects.get(id=1)
            track, created = Track.objects.update_or_create(
                user=user,
                name='{} {} - {}'.format(route['name'], convert_route_time(route['Placemark'][0]['TimeStamp']['when']).date(), convert_route_time(route['Placemark'][-2]['TimeStamp']['when']).date()),
                description='My Track' )
            if created:
                routes += 1
            for point in route['Placemark']:
                try:
                    data = point['ExtendedData']['Data']
                    if not data[15]['value']:
                        point, created = Point.objects.update_or_create(
                            track=track,
                            time=Time.objects.update_or_create(
                                UTC_time = timezone.make_aware(convert_point_time(data[1]['value']), timezone=pytz.UTC), # Convert These '4/15/2017 5:57:19 PM' '4/15/2017 10:57:19 PM'
                                local_time = convert_point_time(data[2]['value']))[0],
                            location=Location.objects.update_or_create(
                                lat=data[8]['value'],
                                lon = data[9]['value'],
                                elevation = convert_elevation(data[10]['value']))[0], #'325 m from MSL'
                            velocity = convert_velocity(data[11]['value']), #'2.5 km/h'
                            course = convert_course(data[12]['value']),
                            # These should likely be something else?
                        )
                        if created:
                            points += 1
                    else:
                        message, created = Message.objects.update_or_create(
                            user=user,
                            time=Time.objects.update_or_create(
                                UTC_time=convert_point_time(data[1]['value']),
                                # Convert These '4/15/2017 5:57:19 PM' '4/15/2017 10:57:19 PM'
                                local_time=convert_point_time(data[2]['value']))[0],
                            location=Location.objects.update_or_create(
                                lat=data[8]['value'],
                                lon=data[9]['value'])[0],
                            text=data[15]['value'],
                            # These should likely be something else?
                        )
                        if created:
                            messages += 1
                except KeyError:
                    pass
        print('\033[92mCreated {} Routes, {} Points and {} Messages'.format(routes, points, messages))

def convert_route_time(time):
    return datetime.strptime(time,'%Y-%m-%dT%H:%M:%SZ',)

def convert_point_time(time):
    return datetime.strptime(time,'%m/%d/%Y %I:%M:%S %p')

def convert_elevation(elevation):
    meters = re.match('[0-9.]*', elevation)[0]
    meters = float(meters)
    return meters * 3.2808398950131

def convert_velocity(velocity):
    velocity = re.match('[0-9.]*', velocity)[0]
    velocity = float(velocity)
    return velocity * 3280.8

def convert_course(course):
    if course:
        course = re.match('[0-9.]*', course)[0]
        return course
    return

"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=256, blank=True, null=True)
    desc = models.TextField(max_length=1000, blank=True, null=True)
"""
""" 
   Make these work with the thingy
   lat = models.FloatField()
    lon = models.FloatField()
    datetime = models.DateTimeField()
    elevation = models.FloatField(blank=True)
    velocity = models.FloatField(blank=True)
    course = models.CharField(max_length=5, blank=True, required=False)
    track = models.OneToOneField(to=Track)"""
