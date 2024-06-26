from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            self.stdout.write("Creating admin account...")
            User.objects.create_superuser(
                username="admin",
                email="admin@mail.ru",
                first_name="admin",
                last_name="admin",
                password="admin",
            )
            self.stdout.write(self.style.SUCCESS("Admin account successfully created"))
        else:
            self.stdout.write("Admin account already exists")
