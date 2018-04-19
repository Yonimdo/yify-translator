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
        self.list = self.get_list()
        return self.list.get(language, None)

    def get_list(self):
        self.list = {val.split('¾')[0]: val.split('¾')[1] for val in self.values.split('½') if val is not ""}
        return self.list

    def __str__(self):
        return self.values


class OriginalText(models.Model):
    text = models.ForeignKey(LenguaText, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    original = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['original'], name='raw_original_idx'),
        ]

    def __str__(self):
        return "{}, count = {}".format(self.original, self.count)


class SmartText(models.Model):
    count = models.IntegerField(default=1)
    text = models.TextField()
    language = models.TextField(max_length=2)
    text_origin = models.ForeignKey(LenguaText, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['text'], name='raw_text_idx'),
        ]

    def __str__(self):
        return "{}, count = {}".format(self.text, self.count)


class Suggestion(models.Model):
    original = models.TextField()
    translation = models.TextField()
    user_translation = models.TextField()
    from_language = models.TextField()
    to_language = models.TextField()
    count = models.IntegerField(default=1)

    def __str__(self):
        return "Google: {}, User = {}".format(self.translation, self.user_translation)
