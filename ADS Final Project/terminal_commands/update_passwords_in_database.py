"""
Update passwords in MySQL database (phpMyAdmin) with Django password hashes
This ensures passwords work both in Django and if someone checks phpMyAdmin
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Session
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.db.models import Count

print("="*70)
print("UPDATING PASSWORDS IN MYSQL DATABASE (phpMyAdmin)")
print("="*70)

# Generate Django password hash
TEST_PASSWORD = 'test123'
password_hash = make_password(TEST_PASSWORD)
print(f"\nGenerated password hash for: {TEST_PASSWORD}")
print(f"Hash: {password_hash[:50]}...")

# Get accounts with sessions
students_with_sessions = Student.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count')[:10]

tutors_with_sessions = Tutor.objects.annotate(
    session_count=Count('session')
).filter(session_count__gt=0).order_by('-session_count')[:10]

# Collect all user IDs to update
user_ids = []
for student in students_with_sessions:
    user_ids.append(student.user.id)

for tutor in tutors_with_sessions:
    user_ids.append(tutor.user.id)

print(f"\nUpdating passwords for {len(user_ids)} accounts...")
print("-" * 70)

# Update passwords directly in database
cursor = connection.cursor()

# Update using Django ORM (which will hash properly)
updated_count = 0
for user_id in user_ids:
    try:
        user = User.objects.get(id=user_id)
        user.set_password(TEST_PASSWORD)
        user.save()
        updated_count += 1
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")

print(f"✅ Updated {updated_count} user passwords via Django ORM")

# Also update directly in MySQL to ensure it's in the database
print("\nUpdating passwords directly in MySQL database...")
print("-" * 70)

try:
    # Update all users with sessions
    cursor.execute("""
        UPDATE users u
        INNER JOIN students s ON u.user_id = s.user_id
        INNER JOIN sessions sess ON s.student_id = sess.student_id
        SET u.password = %s
        WHERE u.user_id IN (
            SELECT DISTINCT s2.user_id 
            FROM students s2 
            INNER JOIN sessions sess2 ON s2.student_id = sess2.student_id
        )
    """, (password_hash,))
    student_updates = cursor.rowcount
    
    cursor.execute("""
        UPDATE users u
        INNER JOIN tutors t ON u.user_id = t.user_id
        INNER JOIN sessions sess ON t.tutor_id = sess.tutor_id
        SET u.password = %s
        WHERE u.user_id IN (
            SELECT DISTINCT t2.user_id 
            FROM tutors t2 
            INNER JOIN sessions sess2 ON t2.tutor_id = sess2.tutor_id
        )
    """, (password_hash,))
    tutor_updates = cursor.rowcount
    
    connection.commit()
    
    print(f"✅ Updated {student_updates} student passwords in MySQL")
    print(f"✅ Updated {tutor_updates} tutor passwords in MySQL")
    print(f"✅ Total: {student_updates + tutor_updates} passwords updated in database")
    
except Exception as e:
    print(f"❌ Error updating MySQL: {e}")
    connection.rollback()

# Verify the update
print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

# Test a few accounts
test_accounts = [
    ('rose.gardner338@aol.com', 'Student'),
    ('prof.douglas.nguyen1900@student.edu', 'Tutor'),
]

from django.contrib.auth import authenticate

for email, role in test_accounts:
    user = User.objects.get(email=email)
    result = authenticate(username=email, password=TEST_PASSWORD)
    status = "✅" if result else "❌"
    print(f"{status} {role}: {email} - Login works: {result is not None}")

print("\n" + "="*70)
print("✅ PASSWORD UPDATE COMPLETE!")
print("="*70)
print(f"\nAll accounts with sessions now have password: {TEST_PASSWORD}")
print("\nYou can now:")
print("1. Login in Django app with these accounts")
print("2. See the password hash in phpMyAdmin (it's hashed for security)")
print("3. The password field in phpMyAdmin will show the Django hash")
print("\nNote: Passwords are hashed in the database - this is normal and secure!")
print("="*70)

