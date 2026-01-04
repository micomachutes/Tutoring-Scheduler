"""
Data Population Script for Tutor Session Scheduler
Generates 1,000-2,000 records per table with realistic data
Uses Django ORM for proper user creation with password hashing
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from tutoring_app.models import User, Student, Tutor, Subject, Session
from django.contrib.auth.hashers import make_password

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

# Realistic passwords (simple but varied)
PASSWORDS = [
    'password123', 'Welcome123', 'Student2024', 'Tutor2024', 'Learning123',
    'Study2024', 'Education1', 'Academic2024', 'School123', 'College2024',
    'MyPassword1', 'Secure123', 'Access2024', 'Login123', 'User2024',
    'Test1234', 'Demo2024', 'Sample123', 'Default1', 'ChangeMe123'
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

SUBJECTS = [
    'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English',
    'History', 'Geography', 'Computer Science', 'Programming', 'Data Structures',
    'Algorithms', 'Database Systems', 'Web Development', 'Software Engineering', 'Statistics',
    'Calculus', 'Linear Algebra', 'Discrete Mathematics', 'Operating Systems', 'Networks',
    'Machine Learning', 'Artificial Intelligence', 'Data Science', 'Cybersecurity', 'Mobile Development',
    'Spanish', 'French', 'German', 'Chinese', 'Japanese',
    'Economics', 'Business Management', 'Accounting', 'Finance', 'Marketing',
    'Psychology', 'Sociology', 'Philosophy', 'Literature', 'Art History',
    'Music Theory', 'Physical Education', 'Health Sciences', 'Nursing', 'Medicine',
    'Law', 'Political Science', 'International Relations', 'Anthropology', 'Archaeology'
]

SPECIALIZATIONS = [
    'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English',
    'Computer Science', 'Programming', 'Statistics', 'Calculus', 'Data Science'
]

STATUSES = ['pending', 'approved', 'declined', 'completed']


def populate_subjects(count=None):
    """Populate subjects table"""
    print("Populating subjects...")
    
    # Check if subjects already exist
    existing_count = Subject.objects.count()
    if existing_count > 0:
        print(f"Subjects already exist ({existing_count} records). Skipping...")
        return
    
    subjects_data = [Subject(subject_name=subject) for subject in SUBJECTS]
    Subject.objects.bulk_create(subjects_data)
    print(f"Inserted {len(SUBJECTS)} subjects")


def populate_students(count=1500):
    """Populate students and users tables"""
    print(f"Populating {count} students...")
    
    existing_count = Student.objects.count()
    if existing_count >= count:
        print(f"Students already exist ({existing_count} records). Skipping...")
        return
    
    # Calculate how many more to add
    to_add = count - existing_count
    print(f"Adding {to_add} more students...")
    
    students_to_create = []
    start_num = existing_count + 1
    
    for i in range(start_num, start_num + to_add):
        # Generate realistic name
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f'{first_name} {last_name}'
        
        # Generate realistic email
        email_domain = random.choice(EMAIL_DOMAINS)
        # Use various email formats
        email_format = random.choice([
            f'{first_name.lower()}.{last_name.lower()}@{email_domain}',
            f'{first_name.lower()}{last_name.lower()}@{email_domain}',
            f'{first_name.lower()}{random.randint(1, 999)}@{email_domain}',
            f'{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@{email_domain}'
        ])
        email = email_format
        
        # Generate unique username
        username = f'{first_name.lower()}{last_name.lower()}{i}'
        
        # Use realistic password
        password = random.choice(PASSWORDS)
        
        created_at = datetime.now() - timedelta(days=random.randint(0, 365))
        
        # Create user using Django ORM (properly hashes password)
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,  # Django will hash this automatically
            role='student',
            date_joined=created_at,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create student profile
        student = Student(user=user, full_name=full_name)
        students_to_create.append(student)
        
        if i % 100 == 0:
            Student.objects.bulk_create(students_to_create)
            students_to_create = []
            print(f"Inserted {i} students...")
    
    if students_to_create:
        Student.objects.bulk_create(students_to_create)
    
    print(f"Inserted {to_add} students (Total: {Student.objects.count()})")


def populate_tutors(count=500):
    """Populate tutors and users tables"""
    print(f"Populating {count} tutors...")
    
    existing_count = Tutor.objects.count()
    if existing_count >= count:
        print(f"Tutors already exist ({existing_count} records). Skipping...")
        return
    
    # Calculate how many more to add
    to_add = count - existing_count
    print(f"Adding {to_add} more tutors...")
    
    tutors_to_create = []
    start_num = existing_count + 1
    
    for i in range(start_num, start_num + to_add):
        # Generate realistic name
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f'{first_name} {last_name}'
        
        # Generate realistic email
        email_domain = random.choice(EMAIL_DOMAINS)
        # Use various email formats
        email_format = random.choice([
            f'{first_name.lower()}.{last_name.lower()}@{email_domain}',
            f'{first_name.lower()}{last_name.lower()}@{email_domain}',
            f'{first_name.lower()}{random.randint(1, 999)}@{email_domain}',
            f'prof.{first_name.lower()}.{last_name.lower()}@{email_domain}',
            f'{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@{email_domain}'
        ])
        email = email_format
        
        # Generate unique username
        username = f'{first_name.lower()}{last_name.lower()}{i}'
        
        # Use realistic password
        password = random.choice(PASSWORDS)
        
        specialization = random.choice(SPECIALIZATIONS)
        created_at = datetime.now() - timedelta(days=random.randint(0, 365))
        
        # Create user using Django ORM (properly hashes password)
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,  # Django will hash this automatically
            role='tutor',
            date_joined=created_at,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create tutor profile
        tutor = Tutor(user=user, full_name=full_name, specialization=specialization)
        tutors_to_create.append(tutor)
        
        if i % 100 == 0:
            Tutor.objects.bulk_create(tutors_to_create)
            tutors_to_create = []
            print(f"Inserted {i} tutors...")
    
    if tutors_to_create:
        Tutor.objects.bulk_create(tutors_to_create)
    
    print(f"Inserted {to_add} tutors (Total: {Tutor.objects.count()})")


def populate_sessions(count=2000):
    """Populate sessions table"""
    print(f"Populating {count} sessions...")
    
    existing_count = Session.objects.count()
    if existing_count >= count:
        print(f"Sessions already exist ({existing_count} records). Skipping...")
        return
    
    # Get IDs
    students = list(Student.objects.all())
    tutors = list(Tutor.objects.all())
    subjects = list(Subject.objects.all())
    
    if not students or not tutors or not subjects:
        print("Error: Need students, tutors, and subjects before creating sessions!")
        return
    
    # Calculate how many more to add
    to_add = count - existing_count
    print(f"Adding {to_add} more sessions...")
    
    sessions_to_create = []
    start_num = existing_count + 1
    
    for i in range(start_num, start_num + to_add):
        student = random.choice(students)
        tutor = random.choice(tutors)
        subject = random.choice(subjects)
        
        # Random date (between 30 days ago and 60 days in the future)
        days_offset = random.randint(-30, 60)
        session_date = datetime.now().date() + timedelta(days=days_offset)
        
        # Random time (between 8 AM and 8 PM)
        from datetime import time as dt_time
        hour = random.randint(8, 20)
        minute = random.choice([0, 15, 30, 45])
        session_time = dt_time(hour=hour, minute=minute, second=0)
        
        # Random status (weighted)
        rand_num = random.random()
        if rand_num < 0.3:
            status = 'pending'
        elif rand_num < 0.6:
            status = 'approved'
        elif rand_num < 0.8:
            status = 'completed'
        else:
            status = 'declined'
        
        # Random realistic notes (70% chance)
        notes = random.choice(SESSION_NOTES) if random.random() < 0.7 else None
        
        # Random created_at (up to 60 days ago)
        created_at = datetime.now() - timedelta(days=random.randint(0, 60))
        
        session = Session(
            student=student,
            tutor=tutor,
            subject=subject,
            session_date=session_date,
            session_time=session_time,
            status=status,
            notes=notes,
            created_at=created_at
        )
        sessions_to_create.append(session)
        
        if i % 200 == 0:
            Session.objects.bulk_create(sessions_to_create)
            sessions_to_create = []
            print(f"Inserted {i} sessions...")
    
    if sessions_to_create:
        Session.objects.bulk_create(sessions_to_create)
    
    print(f"Inserted {to_add} sessions (Total: {Session.objects.count()})")


def verify_counts():
    """Verify record counts"""
    print("\n" + "="*50)
    print("Verifying data counts...")
    print("="*50)
    
    user_count = User.objects.count()
    student_count = Student.objects.count()
    tutor_count = Tutor.objects.count()
    subject_count = Subject.objects.count()
    session_count = Session.objects.count()
    
    print(f"Users: {user_count} records")
    print(f"Students: {student_count} records")
    print(f"Tutors: {tutor_count} records")
    print(f"Subjects: {subject_count} records")
    print(f"Sessions: {session_count} records")
    print("="*50)


def main():
    """Main function"""
    try:
        print("="*50)
        print("Data Population Script")
        print("Generating 1,000-2,000 records per table")
        print("="*50)
        
        # Populate tables
        populate_subjects()
        populate_students(count=1500)
        populate_tutors(count=500)
        populate_sessions(count=2000)
        
        # Verify
        verify_counts()
        
        print("\n✅ Data population completed successfully!")
        print("\n📝 Note: All users have realistic names, emails, and passwords.")
        print("   Passwords are randomly selected from a pool of common passwords.")
        print("   To login, check the database for actual email addresses.")
        print("\n💡 Tip: Run this query to see sample accounts:")
        print("   SELECT email, username FROM users LIMIT 10;")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

