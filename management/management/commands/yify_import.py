import re

from tools import yify
from translator import NUMBERS_REGEX

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# ½ ¾
from texts.models import LenguaText, OriginalText, SmartText


class Command(BaseCommand):
    help = '''
    
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--movie',
            action='store_true',
            dest='movie',
            default='Gone',
            help='Search movie names to insert or just mess wit the data',
        )
        parser.add_argument(
            '--limit',
            action='store_true',
            dest='limit',
            default=2,
            help='Limit the result or DDOS attack your call.',
        )

    def handle(self, *args, **options):
        search = options.get('movie')
        limit = options.get('limit')
        results = yify.search_subtitles(search, limit)
