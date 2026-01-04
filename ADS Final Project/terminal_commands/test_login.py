"""
Test login functionality
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User
from django.contrib.auth import authenticate

test_email = 'rose.gardner338@aol.com'
test_password = 'test123'

print("Testing login...")
print(f"Email: {test_email}")
print(f"Password: {test_password}")

result = authenticate(username=test_email, password=test_password)

if result:
    print(f"✅ LOGIN SUCCESSFUL!")
    print(f"   User: {result.email}")
    print(f"   Role: {result.role}")
    print(f"   Name: {result.get_full_name()}")
else:
    print("❌ LOGIN FAILED")
    print("   Password might not be set correctly")

