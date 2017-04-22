import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    help = 'Overwrite Local DB with Heroku Copy'

    def __init__(self):
        super(Command, self).__init__()
        self.get_app_name()
        self.get_db_settings()

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--no_backup',
            action='store_true',
            dest='no_backup',
            default=False,
            help='Do not create a backup of the database on Heroku',
        )

    def handle(self, *args, **options):
        if not options['no_backup']:
            self.backup_db()
        self.download_db()
        self.drop_db()
        self.create_db()
        self.restore_db()

    def get_app_name(self):
        try:
            self.app_name = settings.HEROKU_APP_NAME
        except AttributeError:
            error = 'Please Set HEROKU_APP_NAME var in settings'
            self.stdout.write(self.style.ERROR(error))
            exit()

    def get_db_settings(self):
        db = settings.DATABASES['default']
        self.db_name = db['NAME']
        return db

    def backup_db(self):
        process = subprocess.Popen("heroku pg:backups:capture --app {}".format(self.app_name).split(),
                                   stdout=subprocess.PIPE, cwd=BASE_DIR)
        output, error = process.communicate()
        return output

    def download_db(self):
        process = subprocess.Popen("heroku pg:backups:download --app {}".format(self.app_name).split(),
                                   stdout=subprocess.PIPE, cwd=BASE_DIR)
        output, error = process.communicate()
        return output

    def drop_db(self):
        proc = subprocess.call("psql -c 'DROP DATABASE {};'".format(self.db_name), shell=True, cwd=BASE_DIR)
        return proc

    def create_db(self):
        proc = subprocess.call("psql -c 'CREATE DATABASE {};'".format(self.db_name),
                               shell=True, cwd=BASE_DIR)
        return proc

    def restore_db(self):
        process = subprocess.Popen(
            "pg_restore --verbose --clean --no-acl --no-owner -h localhost -d {} latest.dump".format(
                self.db_name).split(), stdout=subprocess.PIPE, cwd=BASE_DIR)
        output, error = process.communicate()
        return output
