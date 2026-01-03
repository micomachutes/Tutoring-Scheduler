"""
Quick script to view data in Django system
Run: python view_data.py
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Subject, Session

def print_section(title):
    print("\n" + "="*70)
    print(title)
    print("="*70)

def view_data():
    # Summary counts
    print_section("DATABASE SUMMARY")
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Students: {Student.objects.count()}")
    print(f"Total Tutors: {Tutor.objects.count()}")
    print(f"Total Subjects: {Subject.objects.count()}")
    print(f"Total Sessions: {Session.objects.count()}")
    
    # Sample Students
    print_section("SAMPLE STUDENTS (First 10)")
    students = Student.objects.select_related('user').all()[:10]
    for i, student in enumerate(students, 1):
        user = student.user
        print(f"\n{i}. {student.full_name}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   User ID: {user.id}")
        print(f"   Created: {user.date_joined.strftime('%Y-%m-%d') if user.date_joined else 'N/A'}")
    
    # Sample Tutors
    print_section("SAMPLE TUTORS (First 10)")
    tutors = Tutor.objects.select_related('user').all()[:10]
    for i, tutor in enumerate(tutors, 1):
        user = tutor.user
        print(f"\n{i}. {tutor.full_name}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Specialization: {tutor.specialization}")
        print(f"   User ID: {user.id}")
    
    # Sample Sessions
    print_section("SAMPLE SESSIONS (First 10)")
    sessions = Session.objects.select_related('student', 'tutor', 'subject').all()[:10]
    for i, session in enumerate(sessions, 1):
        print(f"\n{i}. Session #{session.session_id}")
        print(f"   Student: {session.student.full_name}")
        print(f"   Tutor: {session.tutor.full_name}")
        print(f"   Subject: {session.subject.subject_name}")
        print(f"   Date: {session.session_date} at {session.session_time}")
        print(f"   Status: {session.status}")
        if session.notes:
            print(f"   Notes: {session.notes[:60]}...")
    
    # Status breakdown
    print_section("SESSION STATUS BREAKDOWN")
    statuses = Session.objects.values('status').annotate(
        count=__import__('django.db.models', fromlist=['Count']).Count('session_id')
    )
    for status in statuses:
        print(f"{status['status'].title()}: {status['count']} sessions")
    
    # Subjects
    print_section("ALL SUBJECTS")
    subjects = Subject.objects.all().order_by('subject_name')
    print(f"Total: {subjects.count()} subjects")
    for i, subject in enumerate(subjects, 1):
        session_count = Session.objects.filter(subject=subject).count()
        print(f"  {i}. {subject.subject_name} ({session_count} sessions)")

if __name__ == '__main__':
    view_data()

