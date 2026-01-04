"""
Show sample accounts with realistic data
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor

print("="*70)
print("SAMPLE STUDENT ACCOUNTS (First 10)")
print("="*70)
students = Student.objects.select_related('user').all()[:10]
for i, student in enumerate(students, 1):
    user = student.user
    print(f"\n{i}. {student.full_name}")
    print(f"   Email: {user.email}")
    print(f"   Username: {user.username}")
    print(f"   Role: {user.role}")

print("\n" + "="*70)
print("SAMPLE TUTOR ACCOUNTS (First 10)")
print("="*70)
tutors = Tutor.objects.select_related('user').all()[:10]
for i, tutor in enumerate(tutors, 1):
    user = tutor.user
    print(f"\n{i}. {tutor.full_name}")
    print(f"   Email: {user.email}")
    print(f"   Username: {user.username}")
    print(f"   Specialization: {tutor.specialization}")
    print(f"   Role: {user.role}")

print("\n" + "="*70)
print("TOTAL COUNTS")
print("="*70)
print(f"Total Students: {Student.objects.count()}")
print(f"Total Tutors: {Tutor.objects.count()}")
print(f"Total Users: {User.objects.count()}")

