from management.tools import yify

from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand

from management.tools import yify


# ½ ¾


class Command(BaseCommand):
    help = '''
    
    '''

    def add_arguments(self, parser):
        parser.add_argument('movie')
        parser.add_argument('limit')


    def handle(self, movie, limit, *args, **options):
        search = options.get('movie')
        results = yify.search_subtitles(search, 2)
