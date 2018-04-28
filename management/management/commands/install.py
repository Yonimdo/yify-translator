from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


# ½ ¾
from lenguatranslator import settings


class Command(BaseCommand):
    help = "Install Super user"

    def handle(self, *args, **options):
        user = User.objects.create_superuser(
        username="admin",
        email='syrmapp@gmail.com',
        password=settings.PASSWORD)
        user.full_clean()
        user.save()
