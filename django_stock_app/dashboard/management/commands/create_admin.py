from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """ Command to create a admin-superuser."""
    def handle(self, *args, **options) -> None:
        if not User.objects.count():
            User.objects.create_superuser(
                username="admin", password="admin", email="admin@admin.com")
