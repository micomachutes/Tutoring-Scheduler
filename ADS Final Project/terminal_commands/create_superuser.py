"""
Create Django superuser with specified credentials
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User

def create_superuser():
    username = 'machutesmicoadmin'
    email = 'machutesmico@admin.com'
    password = 'mM56252698'
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        print("Updating existing user to superuser...")
        user = User.objects.get(username=username)
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save()
        print(f"✅ Updated user '{username}' to superuser")
    elif User.objects.filter(email=email).exists():
        print(f"❌ User with email '{email}' already exists!")
        user = User.objects.get(email=email)
        user.username = username
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save()
        print(f"✅ Updated user with email '{email}' to superuser")
    else:
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully!")
    
    print(f"\n📋 Superuser Details:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n🌐 Access admin at: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    try:
        create_superuser()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

