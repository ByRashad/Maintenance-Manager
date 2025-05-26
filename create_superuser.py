import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_manager.settings')
django.setup()

from django.contrib.auth.models import User

# Create a superuser
User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)

print("Superuser created successfully!")
