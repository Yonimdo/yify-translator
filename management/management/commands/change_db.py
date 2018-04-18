import re
from translator import NUMBERS_REGEX

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


# ½ ¾
from texts.models import LenguaText, OriginalText


class Command(BaseCommand):
    help = "Change the db"

    def handle(self, *args, **options):
        texts = LenguaText.objects.all()
        for text in texts:
            text.values = re.sub(pattern=NUMBERS_REGEX, repl='18', string=text.values)
            text.save()
        orginals = OriginalText.objects.all()
        for og in orginals:
            og.original = re.sub(pattern=NUMBERS_REGEX, repl='18', string=og.original)
            og.save()