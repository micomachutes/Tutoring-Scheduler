"""
Reset passwords for multiple accounts so you can login
This will set passwords to a known value for testing
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
print("RESET PASSWORDS FOR LOGIN TESTING")
print("="*70)

# Common test passwords to try
COMMON_PASSWORDS = [
    'password123', 'Welcome123', 'Student2024', 'Tutor2024', 'Learning123',
    'Study2024', 'Education1', 'Academic2024', 'School123', 'College2024',
    'MyPassword1', 'Secure123', 'Access2024', 'Login123', 'User2024',
    'Test1234', 'Demo2024', 'Sample123', 'Default1', 'ChangeMe123'
]

# Set a simple password for testing
TEST_PASSWORD = 'test123'

print(f"\nSetting password to '{TEST_PASSWORD}' for accounts with sessions...")
print("-" * 70)

# Reset passwords for students with sessions
students_with_sessions = Student.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count')[:10]

print(f"\n1. RESETTING PASSWORDS FOR TOP 10 STUDENTS WITH SESSIONS:")
for i, student in enumerate(students_with_sessions, 1):
    user = student.user
    user.set_password(TEST_PASSWORD)
    user.save()
    session_count = Session.objects.filter(student=student).count()
    print(f"   {i}. {student.full_name}")
    print(f"      Email: {user.email}")
    print(f"      Password: {TEST_PASSWORD}")
    print(f"      Sessions: {session_count}")

# Reset passwords for tutors with sessions
tutors_with_sessions = Tutor.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count')[:10]

print(f"\n2. RESETTING PASSWORDS FOR TOP 10 TUTORS WITH SESSIONS:")
for i, tutor in enumerate(tutors_with_sessions, 1):
    user = tutor.user
    user.set_password(TEST_PASSWORD)
    user.save()
    session_count = Session.objects.filter(tutor=tutor).count()
    print(f"   {i}. {tutor.full_name}")
    print(f"      Email: {user.email}")
    print(f"      Password: {TEST_PASSWORD}")
    print(f"      Sessions: {session_count}")

print("\n" + "="*70)
print("✅ PASSWORDS RESET SUCCESSFULLY!")
print("="*70)
print(f"\nAll accounts above now have password: {TEST_PASSWORD}")
print("\nTo login:")
print("1. Start server: python manage.py runserver")
print("2. Go to: http://127.0.0.1:8000/login/")
print("3. Use any email above with password: test123")
print("\n" + "="*70)

