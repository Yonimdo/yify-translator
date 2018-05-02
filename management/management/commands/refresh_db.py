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
        for text_origin in texts:
            try:
                if '+' in text_origin:
                    text_origin.remove()
            except Exception as e:
                text_origin.delete()
            try:
                if '1818' in text_origin:
                    text_origin.remove()
            except Exception as e:
                text_origin.delete()
