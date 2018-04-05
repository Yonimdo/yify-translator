from django.db import models


# ½ ¾
# Create your models here.

class LenguaText(models.Model):
    uuid = models.CharField(max_length=40)
    values = models.TextField()

    def add_translation(self, text, language):
        list = {val.split('¾')[0]: val.split('¾')[1] for val in self.values.split('½') if val is not ""}
        list[language] = text
        self.values = "½".join(["{}¾{}".format(key, value) for (key, value) in list.items()])

    def get_text(self, language="XX"):
        self.list = {val.split('¾')[0]: val.split('¾')[1] for val in self.values.split('½') if val is not ""}
        return self.list.get(language, None)

    def __str__(self):
        return self.values