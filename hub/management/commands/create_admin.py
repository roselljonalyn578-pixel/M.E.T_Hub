from django.core.management.base import BaseCommand
from hub.models import CustomUser


class Command(BaseCommand):
    help = 'Create admin superuser account'

    def handle(self, *args, **options):
        try:
            username = 'jona'
            email = 'jonalyn.rosell@example.com'
            password = 'pelimer2003'
            first_name = 'Jonalyn'
            last_name = 'Rosell'

            if CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.get(username=username)
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.is_staff = True
                user.is_superuser = True
                user.role = 'admin'
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Updated: {username} - is_staff={user.is_staff}, is_superuser={user.is_superuser}'))
            else:
                user = CustomUser.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role='admin'
                )
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created admin user: {username}'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Admin creation skipped: {e}'))
