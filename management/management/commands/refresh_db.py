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
        for text_origin in texts:
            try:
                en = text_origin.get_text()




                languages = text_origin.get_list()
                for key in languages:
                    text = languages[key]
                    s_text = SmartText()
                    s_text.text_origin = text_origin
                    s_text.language = key
                    s_text.text = text
                    s_text.save()

            except Exception as e:
                text_origin.delete()
