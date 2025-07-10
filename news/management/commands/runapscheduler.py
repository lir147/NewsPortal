from django.core.management.base import BaseCommand
from news.scheduler import run

class Command(BaseCommand):
    help = 'Запускает django-apscheduler'

    def handle(self, *args, **kwargs):
        run()