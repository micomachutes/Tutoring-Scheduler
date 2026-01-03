"""
Show all tutor accounts with their details
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import Tutor, Session
from django.db.models import Count

print("="*70)
print("TUTOR ACCOUNTS IN DATABASE")
print("="*70)

total_tutors = Tutor.objects.count()
tutors_with_sessions = Tutor.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).count()

print(f"\nTotal Tutors: {total_tutors}")
print(f"Tutors with sessions: {tutors_with_sessions}")
print(f"Tutors without sessions: {total_tutors - tutors_with_sessions}")

# Show tutors with most sessions
print("\n" + "="*70)
print("TOP 20 TUTORS WITH MOST SESSIONS")
print("="*70)

tutors = Tutor.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count')[:20]

for i, tutor in enumerate(tutors, 1):
    user = tutor.user
    print(f"\n{i}. {tutor.full_name}")
    print(f"   Email: {user.email}")
    print(f"   Specialization: {tutor.specialization}")
    print(f"   Sessions: {tutor.session_count}")
    print(f"   Password: test123 (if has sessions)")

# Show all specializations
print("\n" + "="*70)
print("TUTOR SPECIALIZATIONS")
print("="*70)

specializations = Tutor.objects.values('specialization').annotate(
    count=Count('tutor_id')
).order_by('-count')

for spec in specializations:
    print(f"  {spec['specialization']}: {spec['count']} tutors")

print("\n" + "="*70)
print(f"YES - Database has {total_tutors} tutor accounts with realistic data!")
print("="*70)

