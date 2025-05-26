import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_manager.settings')
django.setup()

from django.contrib.auth.models import User
from maintenance.models import UserRole, UserProfile

def setup_roles():
    # Create Admin role
    admin_role, _ = UserRole.objects.update_or_create(
        name='admin',
        defaults={
            'can_add_users': True,
            'can_delete_users': True,
            'can_view_all': True,
            'can_export': True
        }
    )
    
    # Create Technician role
    tech_role, _ = UserRole.objects.update_or_create(
        name='technician',
        defaults={
            'can_add_users': False,
            'can_delete_users': False,
            'can_view_all': True,
            'can_export': True
        }
    )
    
    # Update existing users' roles
    for user in User.objects.all():
        # Create user profile if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        if user.is_superuser:
            profile.role = admin_role
        else:
            profile.role = tech_role
        
        profile.save()

if __name__ == '__main__':
    setup_roles()
