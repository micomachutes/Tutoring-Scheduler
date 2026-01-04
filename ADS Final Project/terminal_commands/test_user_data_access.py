"""
Test if logged-in users can see their data in the Django app
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Session

print("="*70)
print("TESTING USER DATA ACCESS IN DJANGO APP")
print("="*70)

# Test Student Access
print("\n1. TESTING STUDENT ACCOUNTS:")
print("-" * 70)
students_with_sessions = Student.objects.annotate(
    session_count=__import__('django.db.models', fromlist=['Count']).Count('session')
).filter(session_count__gt=0)[:5]

if students_with_sessions:
    print(f"Found {students_with_sessions.count()} students with sessions")
    for student in students_with_sessions:
        session_count = Session.objects.filter(student=student).count()
        print(f"\n  Student: {student.full_name}")
        print(f"  Email: {student.user.email}")
        print(f"  Total Sessions: {session_count}")
        print(f"  Pending: {Session.objects.filter(student=student, status='pending').count()}")
        print(f"  Approved: {Session.objects.filter(student=student, status='approved').count()}")
        print(f"  ✅ This student WILL see data when logged in")
else:
    print("  ⚠️  No students have sessions assigned!")

# Test Tutor Access
print("\n2. TESTING TUTOR ACCOUNTS:")
print("-" * 70)
tutors_with_sessions = Tutor.objects.annotate(
    session_count=__import__('django.db.models', fromlist=['Count']).Count('session')
).filter(session_count__gt=0)[:5]

if tutors_with_sessions:
    print(f"Found {tutors_with_sessions.count()} tutors with sessions")
    for tutor in tutors_with_sessions:
        session_count = Session.objects.filter(tutor=tutor).count()
        print(f"\n  Tutor: {tutor.full_name}")
        print(f"  Email: {tutor.user.email}")
        print(f"  Total Sessions: {session_count}")
        print(f"  Pending: {Session.objects.filter(tutor=tutor, status='pending').count()}")
        print(f"  Approved: {Session.objects.filter(tutor=tutor, status='approved').count()}")
        print(f"  ✅ This tutor WILL see data when logged in")
else:
    print("  ⚠️  No tutors have sessions assigned!")

# Check session distribution
print("\n3. SESSION DISTRIBUTION:")
print("-" * 70)
total_sessions = Session.objects.count()
students_with_sessions_count = Student.objects.filter(session__isnull=False).distinct().count()
tutors_with_sessions_count = Tutor.objects.filter(session__isnull=False).distinct().count()

print(f"Total Sessions: {total_sessions}")
print(f"Students with sessions: {students_with_sessions_count} / {Student.objects.count()}")
print(f"Tutors with sessions: {tutors_with_sessions_count} / {Tutor.objects.count()}")

# Find accounts to test with
print("\n4. RECOMMENDED TEST ACCOUNTS:")
print("-" * 70)
if students_with_sessions.exists():
    test_student = list(students_with_sessions)[0]
    student_sessions = Session.objects.filter(student=test_student).count()
    print(f"\n  STUDENT ACCOUNT (has {student_sessions} sessions):")
    print(f"  Email: {test_student.user.email}")
    print(f"  Password: Check database or use any from password pool")
    print(f"  Login at: http://127.0.0.1:8000/login/")
    print(f"  Will see: Dashboard with {student_sessions} sessions")

if tutors_with_sessions.exists():
    test_tutor = list(tutors_with_sessions)[0]
    tutor_sessions = Session.objects.filter(tutor=test_tutor).count()
    print(f"\n  TUTOR ACCOUNT (has {tutor_sessions} sessions):")
    print(f"  Email: {test_tutor.user.email}")
    print(f"  Password: Check database or use any from password pool")
    print(f"  Login at: http://127.0.0.1:8000/login/")
    print(f"  Will see: Dashboard with {tutor_sessions} sessions")

print("\n" + "="*70)
print("NOTE: The Django app shows data PER USER.")
print("Each user only sees THEIR OWN sessions, not all sessions.")
print("="*70)

