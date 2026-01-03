"""
Troubleshoot Django Admin Data Display Issues
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Subject, Session
from django.contrib import admin

print("="*70)
print("DJANGO ADMIN TROUBLESHOOTING")
print("="*70)

# Check data exists
print("\n1. CHECKING DATA IN DATABASE:")
print("-" * 70)
print(f"   Users: {User.objects.count()}")
print(f"   Students: {Student.objects.count()}")
print(f"   Tutors: {Tutor.objects.count()}")
print(f"   Subjects: {Subject.objects.count()}")
print(f"   Sessions: {Session.objects.count()}")

# Check admin registration
print("\n2. CHECKING ADMIN REGISTRATION:")
print("-" * 70)
admin_site = admin.site
registered_models = [model.__name__ for model in admin_site._registry.keys()]
print(f"   Registered models: {', '.join(registered_models)}")

# Check if models are registered
models_to_check = ['User', 'Student', 'Tutor', 'Subject', 'Session']
for model_name in models_to_check:
    model = globals()[model_name]
    is_registered = model in admin_site._registry
    status = "✅" if is_registered else "❌"
    print(f"   {status} {model_name}: {'Registered' if is_registered else 'NOT Registered'}")

# Check superuser
print("\n3. CHECKING SUPERUSER:")
print("-" * 70)
superusers = User.objects.filter(is_superuser=True)
print(f"   Total superusers: {superusers.count()}")
for su in superusers:
    print(f"   - {su.username} ({su.email}) - Staff: {su.is_staff}, Active: {su.is_active}")

# Test queries
print("\n4. TESTING DATA ACCESS:")
print("-" * 70)
try:
    sample_user = User.objects.first()
    print(f"   ✅ Can access User: {sample_user}")
except Exception as e:
    print(f"   ❌ Error accessing User: {e}")

try:
    sample_student = Student.objects.first()
    print(f"   ✅ Can access Student: {sample_student}")
except Exception as e:
    print(f"   ❌ Error accessing Student: {e}")

try:
    sample_tutor = Tutor.objects.first()
    print(f"   ✅ Can access Tutor: {sample_tutor}")
except Exception as e:
    print(f"   ❌ Error accessing Tutor: {e}")

try:
    sample_subject = Subject.objects.first()
    print(f"   ✅ Can access Subject: {sample_subject}")
except Exception as e:
    print(f"   ❌ Error accessing Subject: {e}")

try:
    sample_session = Session.objects.first()
    print(f"   ✅ Can access Session: {sample_session}")
except Exception as e:
    print(f"   ❌ Error accessing Session: {e}")

# Recommendations
print("\n5. RECOMMENDATIONS:")
print("-" * 70)
if User.objects.count() > 0:
    print("   ✅ Data exists in database")
    print("\n   To view data in Django Admin:")
    print("   1. Make sure server is running: python manage.py runserver")
    print("   2. Go to: http://127.0.0.1:8000/admin/")
    print("   3. Login with superuser credentials:")
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser:
        print(f"      Username: {superuser.username}")
        print(f"      Email: {superuser.email}")
    print("   4. Click on each model (Users, Students, Tutors, etc.)")
    print("   5. If still empty, try:")
    print("      - Clear browser cache")
    print("      - Try different browser")
    print("      - Check browser console for errors")
else:
    print("   ❌ No data found! Run: python populate_data.py")

print("\n" + "="*70)

