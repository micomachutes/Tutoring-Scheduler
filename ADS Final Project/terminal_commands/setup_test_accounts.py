"""
Setup test accounts with known passwords for testing
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Session
from django.db.models import Count

print("="*70)
print("SETTING UP TEST ACCOUNTS WITH KNOWN PASSWORDS")
print("="*70)

# Find student with most sessions
student_with_sessions = Student.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count').first()

# Find tutor with most sessions
tutor_with_sessions = Tutor.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count').first()

test_password = 'test123'

print("\n1. SETTING UP STUDENT TEST ACCOUNT:")
print("-" * 70)
if student_with_sessions:
    user = student_with_sessions.user
    user.set_password(test_password)
    user.save()
    session_count = Session.objects.filter(student=student_with_sessions).count()
    print(f"✅ Student Account Ready:")
    print(f"   Name: {student_with_sessions.full_name}")
    print(f"   Email: {user.email}")
    print(f"   Password: {test_password}")
    print(f"   Sessions: {session_count}")
    print(f"   Login at: http://127.0.0.1:8000/login/")
else:
    print("❌ No students with sessions found")

print("\n2. SETTING UP TUTOR TEST ACCOUNT:")
print("-" * 70)
if tutor_with_sessions:
    user = tutor_with_sessions.user
    user.set_password(test_password)
    user.save()
    session_count = Session.objects.filter(tutor=tutor_with_sessions).count()
    print(f"✅ Tutor Account Ready:")
    print(f"   Name: {tutor_with_sessions.full_name}")
    print(f"   Email: {user.email}")
    print(f"   Password: {test_password}")
    print(f"   Sessions: {session_count}")
    print(f"   Login at: http://127.0.0.1:8000/login/")
else:
    print("❌ No tutors with sessions found")

print("\n" + "="*70)
print("TEST ACCOUNTS READY!")
print("="*70)
print("\nTo test the Django app:")
print("1. Start server: python manage.py runserver")
print("2. Go to: http://127.0.0.1:8000/login/")
print("3. Login with one of the accounts above")
print("4. You should see data in the dashboard!")
print("\n" + "="*70)

