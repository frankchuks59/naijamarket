# accounts/management/commands/createsuperuser_auto.py
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
import os

class Command(BaseCommand):
    help = 'Create superuser automatically for production'

    def handle(self, *args, **kwargs):
        # Check if superuser already exists
        if CustomUser.objects.filter(is_staff=True, is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists!'))
            return
        
        # Get credentials from environment variables
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@naijamarket.com')
        password = os.getenv('ADMIN_PASSWORD', 'Admin123456!')
        
        # Create superuser
        try:
            CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
            self.stdout.write(self.style.WARNING(f'Email: {email}'))
            self.stdout.write(self.style.WARNING(f'Password: {password}'))
            self.stdout.write(self.style.ERROR('CHANGE THESE CREDENTIALS IMMEDIATELY!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))