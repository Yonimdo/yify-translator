import re
import translator as trns

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# ½ ¾
from texts.models import LenguaText, OriginalText, SmartText


class Command(BaseCommand):
    help = "Normalize the db"

    def handle(self, *args, **options):

        texts = LenguaText.objects.all()
        # remove all funny numbers.
        for t in texts:
            try:
                if '<br>' in t.values:
                    t.values = t.values.replace("<br>"," ")
                    # you are right...
                    t.save()
            except Exception as e:
                print("Error {} at {}".format(e, t))
