from contextlib import closing

import environ
from django.core.management.base import BaseCommand
from psycopg2 import connect
from psycopg2.errorcodes import DUPLICATE_DATABASE, DUPLICATE_OBJECT
from psycopg2 import errors
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

env = environ.Env()

TIMEOUT = 10

class Command(BaseCommand):
    help = 'Creates a new database'

    def add_arguments(self, parser):
        parser.add_argument(
            "--db-url",
            required=True,
            type=str,
            help="Database instance connection url",
        )
        parser.add_argument(
            "--db-name",
            required=True,
            type=str,
            help="New database name",
        )
        parser.add_argument(
            "--db-username",
            required=True,
            type=str,
            help="New database user username",
        )
        parser.add_argument(
            "--db-password",
            required=True,
            type=str,
            help="New database user password",
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting db creation'))

        db_config = env.db_url_config(url=kwargs['db_url'])

        dbname = db_config['NAME']
        user = db_config['USER']
        password = db_config['PASSWORD']
        host = db_config['HOST']

        new_db_name = kwargs['db_name']
        new_db_username = kwargs['db_username']
        new_db_password = kwargs['db_password']

        with closing(connect(dbname=dbname, user=user, host=host, password=password, connect_timeout=TIMEOUT)) as con:
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with con.cursor() as cur:
                try:
                    cur.execute(f'CREATE DATABASE {new_db_name};')
                except errors.lookup(DUPLICATE_DATABASE):
                    self.stdout.write(self.style.WARNING(f'Database "{new_db_name}" already exists. Continuing...'))
                try:
                    cur.execute(f'CREATE USER {new_db_username} WITH ENCRYPTED PASSWORD \'{new_db_password}\';')
                except errors.lookup(DUPLICATE_OBJECT):
                    self.stdout.write(self.style.WARNING(f'User "{new_db_username}" already exists. Continuing...'))
                try:
                    cur.execute(f'GRANT ALL PRIVILEGES ON DATABASE {new_db_name} to {new_db_username};')
                    cur.execute(f'ALTER USER {new_db_username} CREATEDB;')
                except Exception:
                    self.stdout.write(self.style.ERROR(f'Error while granting user "{new_db_username}" privileges.'))
                    raise

                new_db_url = f'postgres://{new_db_username}:{new_db_password}@{host}:5432/{new_db_name}'
                self.stdout.write(self.style.SUCCESS((f'Successfully setup new DB "{new_db_name}". '
                                                      f'New db url: "{new_db_url}"')))
