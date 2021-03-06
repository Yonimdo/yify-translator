import re

from movies.tools import yify, subs
from movies.tools.subs import OrderBy
from translator import NUMBERS_REGEX

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# ½ ¾
from texts.models import LenguaText, OriginalText, SmartText

en = "asdfasdvnsd;kfjvn'dflv,DS:fg.sd" \
     "'fg.s"


class Command(BaseCommand):
    help = '''
 Translate from subtitle!
 Please pick a folder you have imported and see the generated file
 Or check its log in the md file
 --import: Push json to database
 --dir: Create a json from dir
 --sort: Index the Subtitle by [fromto(DEFAULT), pk,from,to, all] may produce variations!!!
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--import',
            action='store',
            dest='import',
            help='Push json to database',
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
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Create a json to all folders',
        )

    def handle(self, *args, **options):
        dir = options.get('dir')
        imp = options.get('import')
        all = options.get('all')
        if dir is None and imp is None:
            print(self.help)
            print("Options:\n")
            print("\t--dir\n\t\t", end="")
            print("\n\t\t".join(subs.get_options()))
            print("\t--import\n\t\t", end="")
            print("\n\t\t".join(subs.get_import_options()))


        order = options.get('order')
        if imp:
            subs.insert_lengua_text(subs.get_json(imp, order))

        if all:
            folders = subs.get_options()
            while folders:
                subs.create_json_from_folder(folders.pop(), OrderBy.getsort(order))
        else:
            subs.create_json_from_folder(dir, OrderBy.getsort(order))
