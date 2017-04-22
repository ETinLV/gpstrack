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



    def handle(self, *args, **options):
        self.dump_db()
        self.push_db()

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

    def dump_db(self):
        process = subprocess.Popen("heroku pg:reset --app {} --confirm {}".format(self.app_name, self.app_name).split(),
                                       stdout=subprocess.PIPE, cwd=BASE_DIR)
        output, error = process.communicate()
        process.wait()
        return output

    def push_db(self):
        process = subprocess.Popen("pg_dump --no-acl --no-owner -h localhost {}".format(self.db_name).split(),
                                       stdout=subprocess.PIPE, cwd=BASE_DIR)
        process2 = subprocess.Popen('heroku pg:psql --app {}'.format(self.app_name).split(), stdin=process.stdout, stdout=subprocess.PIPE)
        output, error = process2.communicate()
        return output
    #
    # def dump_db(self):
    #     process = subprocess.Popen("pg_dump --no-acl --no-owner -h localhost --format=p {} -f {}.dump".format(self.db_name, self.db_name).split(),
    #                                stdout=subprocess.PIPE, cwd=BASE_DIR)
    #     print(process.args)
    #     output, error = process.communicate()
    #     return output
    #
    #
    # def push_db(self):
    #     print('Please Upload the {}.dump file to an HTTP available source.'.format(self.db_name))
    #     url = input('What is the URL of the dump file?\n')
    #     print(url)
    #     process = subprocess.Popen(
    #         "heroku pg:backups:restore {} DATABASE_URL --app {} --confirm {}".format(
    #             url, self.app_name, self.app_name).split(), stdout=subprocess.PIPE, cwd=BASE_DIR)
    #     output, error = process.communicate()
    #     return output
