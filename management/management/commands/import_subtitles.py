import re

from management.tools import yify, subs
from management.tools.subs import OrderBy
from translator import NUMBERS_REGEX

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# ½ ¾
from texts.models import LenguaText, OriginalText, SmartText


class Command(BaseCommand):
    help = '''
        Translate from subtitle!
        Please pick a folder you have imported and see the generated file
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--import',
            action='store',
            dest='import',
            help='Create a json from dir',
        )
        parser.add_argument(
            '--dir',
            action='store',
            dest='dir',
            help='Create a json from dir',
        )
        parser.add_argument(
            '--sort',
            action='store',
            dest='order',
            default='fromto',
            help='Index the Subtitle by [fromto(DEFAULT), pk,from,to, all] may produce variations!!!',
        )

    def handle(self, *args, **options):

        dir = options.get('dir')
        if dir is None:
            print("Options:\n")
            print("\n".join(subs.get_options()))
            print("\n")
            return
        order = options.get('order')
        results = subs.get_folder_data(dir, OrderBy.getsort(order))
        pass
