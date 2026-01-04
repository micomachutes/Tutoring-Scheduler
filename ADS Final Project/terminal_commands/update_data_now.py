"""
Update existing data to realistic names, emails, and notes
Non-interactive version - runs automatically
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Session

# Realistic first names
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
    'Kenneth', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa',
    'Timothy', 'Deborah', 'Ronald', 'Stephanie', 'Jason', 'Rebecca', 'Edward', 'Sharon',
    'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
    'Nicholas', 'Angela', 'Eric', 'Shirley', 'Jonathan', 'Brenda', 'Stephen', 'Emma',
    'Larry', 'Olivia', 'Justin', 'Catherine', 'Scott', 'Christine', 'Brandon', 'Samantha',
    'Benjamin', 'Debra', 'Samuel', 'Rachel', 'Frank', 'Carolyn', 'Gregory', 'Janet',
    'Raymond', 'Virginia', 'Alexander', 'Maria', 'Patrick', 'Heather', 'Jack', 'Diane',
    'Dennis', 'Julie', 'Jerry', 'Joyce', 'Tyler', 'Victoria', 'Aaron', 'Kelly',
    'Jose', 'Christina', 'Henry', 'Joan', 'Adam', 'Evelyn', 'Douglas', 'Judith',
    'Nathan', 'Megan', 'Zachary', 'Cheryl', 'Kyle', 'Andrea', 'Noah', 'Hannah',
    'Ethan', 'Jacqueline', 'Jeremy', 'Martha', 'Walter', 'Gloria', 'Christian', 'Teresa',
    'Keith', 'Sara', 'Roger', 'Janice', 'Terry', 'Marie', 'Austin', 'Julia',
    'Sean', 'Grace', 'Gerald', 'Judy', 'Carl', 'Theresa', 'Harold', 'Madison',
    'Lawrence', 'Beverly', 'Dylan', 'Denise', 'Jesse', 'Marilyn', 'Jordan', 'Amber',
    'Bryan', 'Danielle', 'Billy', 'Rose', 'Joe', 'Brittany', 'Bruce', 'Diana',
    'Gabriel', 'Abigail', 'Logan', 'Jane', 'Alan', 'Lori', 'Juan', 'Lauren',
    'Wayne', 'Mia', 'Ralph', 'Alice', 'Roy', 'Jacqueline', 'Eugene', 'Kristin',
    'Louis', 'Sophia', 'Randy', 'Emma', 'Vincent', 'Olivia', 'Russell', 'Cynthia',
    'Philip', 'Marie', 'Bobby', 'Janet', 'Johnny', 'Catherine', 'Bradley', 'Frances',
    'Willie', 'Ann', 'Oscar', 'Kathryn', 'Alan', 'Rachel', 'Ralph', 'Samantha'
]

# Realistic last names
LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
    'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Sanchez',
    'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
    'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams',
    'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
    'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards',
    'Collins', 'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez',
    'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Reed', 'Bailey', 'Bell', 'Gomez',
    'Kelly', 'Howard', 'Ward', 'Cox', 'Diaz', 'Richardson', 'Wood', 'Watson',
    'Brooks', 'Bennett', 'Gray', 'James', 'Reyes', 'Cruz', 'Hughes', 'Price',
    'Myers', 'Long', 'Foster', 'Sanders', 'Ross', 'Morales', 'Powell', 'Sullivan',
    'Russell', 'Ortiz', 'Jenkins', 'Gutierrez', 'Perry', 'Butler', 'Barnes', 'Fisher',
    'Henderson', 'Coleman', 'Simmons', 'Patterson', 'Jordan', 'Reynolds', 'Hamilton', 'Graham',
    'Kim', 'Gonzales', 'Alexander', 'Ramos', 'Wallace', 'Griffin', 'West', 'Cole',
    'Hayes', 'Chavez', 'Gibson', 'Bryant', 'Ellis', 'Stevens', 'Murray', 'Ford',
    'Marshall', 'Owens', 'Mcdonald', 'Harrison', 'Ruiz', 'Kennedy', 'Wells', 'Alvarez',
    'Woods', 'Mendoza', 'Castillo', 'Olson', 'Webb', 'Washington', 'Tucker', 'Freeman',
    'Burns', 'Henry', 'Vasquez', 'Snyder', 'Simpson', 'Crawford', 'Jimenez', 'Porter',
    'Mason', 'Shaw', 'Gordon', 'Wagner', 'Hunter', 'Romero', 'Hicks', 'Dixon',
    'Hunt', 'Palmer', 'Robertson', 'Black', 'Holmes', 'Stone', 'Meyer', 'Boyd',
    'Mills', 'Warren', 'Fox', 'Rose', 'Rice', 'Moreno', 'Schmidt', 'Patel',
    'Ferguson', 'Nichols', 'Herrera', 'Medina', 'Ryan', 'Fernandez', 'Weaver', 'Daniels',
    'Stephens', 'Gardner', 'Payne', 'Kelley', 'Dunn', 'Pierce', 'Arnold', 'Tran'
]

# Realistic email domains
EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com',
    'mail.com', 'aol.com', 'protonmail.com', 'live.com', 'msn.com',
    'student.edu', 'university.edu', 'college.edu', 'school.edu',
    'email.com', 'ymail.com', 'zoho.com', 'gmx.com', 'yandex.com'
]

# Realistic session notes
SESSION_NOTES = [
    'Need help with calculus homework on derivatives and integrals.',
    'Struggling with understanding database normalization concepts.',
    'Review session for upcoming midterm exam in linear algebra.',
    'Need clarification on object-oriented programming principles.',
    'Help with essay writing and thesis statement development.',
    'Practice problems for organic chemistry reactions.',
    'Understanding statistical hypothesis testing methods.',
    'Review of Spanish verb conjugations in past tense.',
    'Help with understanding machine learning algorithms.',
    'Preparation for physics exam on thermodynamics.',
    'Need assistance with web development project using React.',
    'Review session for data structures and algorithms exam.',
    'Help with understanding financial accounting principles.',
    'Practice problems for differential equations.',
    'Clarification on network protocols and OSI model.',
    'Essay review and feedback on literature analysis.',
    'Help with understanding molecular biology concepts.',
    'Review of French grammar and vocabulary.',
    'Practice coding problems for technical interview preparation.',
    'Understanding probability and statistics distributions.',
    'Help with research paper on psychology theories.',
    'Review session for chemistry lab report writing.',
    'Clarification on software engineering design patterns.',
    'Practice problems for discrete mathematics.',
    'Help with understanding economic models and theories.',
    'Review of history essay on World War II.',
    'Assistance with understanding computer networks.',
    'Help with biology lab experiment analysis.',
    'Review session for English literature exam.',
    'Practice problems for advanced calculus.',
    'Clarification on database query optimization.',
    'Help with understanding artificial intelligence concepts.',
    'Review of programming project code structure.',
    'Assistance with statistics project data analysis.',
    'Help with understanding operating systems concepts.',
    'Practice problems for chemistry final exam.',
    'Review session for mathematics competition preparation.',
    'Clarification on software testing methodologies.',
    'Help with understanding cybersecurity principles.',
    'Review of research methodology for thesis.',
    'Assistance with understanding quantum physics.',
    'Practice problems for computer science algorithms.',
    'Help with essay writing on philosophy topics.',
    'Review session for language proficiency exam.',
    'Clarification on data science machine learning models.',
    'Help with understanding business management concepts.',
    'Review of programming assignment debugging.',
    'Assistance with understanding medical terminology.',
    'Practice problems for engineering mathematics.',
    'Help with understanding legal case studies.'
]

def generate_realistic_email(first_name, last_name, user_id):
    """Generate realistic email address"""
    email_domain = random.choice(EMAIL_DOMAINS)
    formats = [
        f'{first_name.lower()}.{last_name.lower()}@{email_domain}',
        f'{first_name.lower()}{last_name.lower()}@{email_domain}',
        f'{first_name.lower()}{random.randint(1, 999)}@{email_domain}',
        f'{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@{email_domain}'
    ]
    if user_id % 10 == 0:  # Every 10th user gets professor-style email for tutors
        formats.append(f'prof.{first_name.lower()}.{last_name.lower()}@{email_domain}')
    return random.choice(formats)

def update_students():
    """Update students with realistic data"""
    print("Updating students with realistic names and emails...")
    students = Student.objects.select_related('user').all()
    total = students.count()
    updated = 0
    
    for i, student in enumerate(students, 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f'{first_name} {last_name}'
        
        # Update student
        student.full_name = full_name
        student.save()
        
        # Update user
        user = student.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = generate_realistic_email(first_name, last_name, user.id)
        user.username = f'{first_name.lower()}{last_name.lower()}{user.id}'
        user.save()
        updated += 1
        
        if i % 100 == 0:
            print(f"Updated {i}/{total} students...")
    
    print(f"✅ Updated {updated} students")

def update_tutors():
    """Update tutors with realistic data"""
    print("Updating tutors with realistic names and emails...")
    tutors = Tutor.objects.select_related('user').all()
    total = tutors.count()
    updated = 0
    
    for i, tutor in enumerate(tutors, 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f'{first_name} {last_name}'
        
        # Update tutor
        tutor.full_name = full_name
        tutor.save()
        
        # Update user
        user = tutor.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = generate_realistic_email(first_name, last_name, user.id)
        user.username = f'{first_name.lower()}{last_name.lower()}{user.id}'
        user.save()
        updated += 1
        
        if i % 100 == 0:
            print(f"Updated {i}/{total} tutors...")
    
    print(f"✅ Updated {updated} tutors")

def update_sessions():
    """Update sessions with realistic notes"""
    print("Updating sessions with realistic notes...")
    sessions = Session.objects.all()
    total = sessions.count()
    updated = 0
    
    for i, session in enumerate(sessions, 1):
        # 70% chance of having notes
        if random.random() < 0.7:
            session.notes = random.choice(SESSION_NOTES)
        else:
            session.notes = None
        session.save()
        updated += 1
        
        if i % 200 == 0:
            print(f"Updated {i}/{total} sessions...")
    
    print(f"✅ Updated {updated} sessions")

def main():
    print("="*70)
    print("UPDATING EXISTING DATA TO REALISTIC VALUES")
    print("="*70)
    print("\nThis will update:")
    print("  - Student names and emails")
    print("  - Tutor names and emails")
    print("  - Session notes")
    print("\n⏳ Starting update process...\n")
    
    try:
        update_students()
        print()
        update_tutors()
        print()
        update_sessions()
        
        print("\n" + "="*70)
        print("✅ All data updated successfully!")
        print("="*70)
        print("\n📋 Summary:")
        print(f"   - Students: {Student.objects.count()} records updated")
        print(f"   - Tutors: {Tutor.objects.count()} records updated")
        print(f"   - Sessions: {Session.objects.count()} records updated")
        print("\n💡 You can now check phpMyAdmin to see the realistic data!")
        print("   Or run: python show_sample_accounts.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

