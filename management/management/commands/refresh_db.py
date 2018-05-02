import re
import translator as trns

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# ½ ¾
from texts.models import LenguaText, OriginalText, SmartText


class Command(BaseCommand):
    help = "Normalize the db"

    def handle(self, *args, **options):

        texts = OriginalText.objects.all()
        # remove all funny numbers.
        for orig in texts:
            try:
                if '+' in orig.original:
                    orig.remove()
            except Exception as e:
                print("Error at {}".format(orig) )

