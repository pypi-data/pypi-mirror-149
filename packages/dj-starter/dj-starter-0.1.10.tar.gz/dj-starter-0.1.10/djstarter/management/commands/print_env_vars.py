import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Print Environmental Variables'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('### START Environmental Settings ####'))
        for k, v in os.environ.items():
            self.stdout.write(self.style.SUCCESS(f'{k}={v}'))
        self.stdout.write(self.style.WARNING('### END Environmental Settings ####'))
