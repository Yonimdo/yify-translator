from django.db import models

# Create your models here.
import translator
from movies.tools import subs
from texts.models import LenguaText


def import_json(name):
    json = subs.get_json(name)
    if json:
        for key in json:
            values = json[key]
            if 'en' not in values.keys():
                return
            lt = LenguaText()
            for lang in values:
                text = values[lang]
                lt.add_translation(text, lang)
            if not translator.get_lengua_result(None, '', lt.get_text('en')):
                lt.save()
        doc = subs.get_doc(name)
        mr = MovieReport()
        mr.name = name
        mr.doc = doc
        mr.save()


class MovieReport(models.Model):
    name = models.TextField(blank=False, null=False)
    doc = models.TextField(blank=False, null=False)

    # Todo: fields from the user.
    def __str__(self):
        return "{}".format(self.func_name)
