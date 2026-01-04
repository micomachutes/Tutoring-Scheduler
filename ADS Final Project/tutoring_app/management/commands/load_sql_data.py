import os
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from tutoring_app.models import User, Student, Tutor, Subject, Session

class Command(BaseCommand):
    help = 'Loads advanced SQL features and ensures 2000+ records exist'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting data population and SQL feature installation...'))
        
        # 1. Install Advanced SQL Features
        self.install_sql_features()
        
        # 2. Populate Data
        self.populate_data()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded SQL features and data!'))

    def install_sql_features(self):
        self.stdout.write('Installing advanced SQL features...')
        file_path = os.path.join('sql', 'advanced_features.sql')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple parser for DELIMITER
        statements = []
        delimiter = ';'
        buffer = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            if line.upper().startswith('DELIMITER'):
                delimiter = line.split()[1]
                continue
            
            buffer.append(line)
            
            if line.endswith(delimiter):
                # Remove delimiter from the end
                statement = ' '.join(buffer)
                # Cut off the delimiter
                statement = statement[:-len(delimiter)].strip()
                if statement:
                    statements.append(statement)
                buffer = []
        
        # Execute statements
        with connection.cursor() as cursor:
            for sql in statements:
                # Skip USE statement as we are already connected
                if sql.upper().startswith('USE'):
                    continue
                try:
                    cursor.execute(sql)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error executing SQL: {e}\nSQL: {sql[:50]}...'))

    def populate_data(self):
        self.stdout.write('Checking existing data...')
        
        # Check counts
        if Session.objects.count() >= 2000:
            self.stdout.write(self.style.SUCCESS('Data already exists (2000+ sessions). Skipping population.'))
            return

        self.stdout.write('Populating data...')
        
        with transaction.atomic():
            # Subjects
            subjects = [
                'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English',
                'History', 'Geography', 'Computer Science', 'Programming', 'Data Structures',
                'Algorithms', 'Database Systems', 'Web Development', 'Software Engineering', 'Statistics',
                'Calculus', 'Linear Algebra', 'Discrete Mathematics', 'Operating Systems', 'Networks',
                'Machine Learning', 'Artificial Intelligence', 'Data Science', 'Cybersecurity', 'Mobile Development',
                'Spanish', 'French', 'German', 'Chinese', 'Japanese',
                'Economics', 'Business Management', 'Accounting', 'Finance', 'Marketing',
                'Psychology', 'Sociology', 'Philosophy', 'Literature', 'Art History'
            ]
            
            existing_subjects = set(Subject.objects.values_list('subject_name', flat=True))
            new_subjects = [Subject(subject_name=s) for s in subjects if s not in existing_subjects]
            Subject.objects.bulk_create(new_subjects)
            all_subjects = list(Subject.objects.all())
            
            # Users & Students (Target 200)
            existing_students_count = Student.objects.count()
            students_needed = max(0, 200 - existing_students_count)
            all_students = []
            
            if students_needed > 0:
                self.stdout.write(f'Creating {students_needed} students...')
                for i in range(students_needed):
                    email = f'student_{timezone.now().timestamp()}_{i}@example.com'
                    user = User.objects.create(
                        username=email,
                        email=email,
                        password=make_password('password'),
                        role='student'
                    )
                    student = Student.objects.create(
                        user=user,
                        full_name=f'Student {i+existing_students_count+1}'
                    )
                    all_students.append(student)
            else:
                all_students = list(Student.objects.all())

            # Users & Tutors (Target 50)
            existing_tutors_count = Tutor.objects.count()
            tutors_needed = max(0, 50 - existing_tutors_count)
            all_tutors = []
            
            if tutors_needed > 0:
                self.stdout.write(f'Creating {tutors_needed} tutors...')
                for i in range(tutors_needed):
                    email = f'tutor_{timezone.now().timestamp()}_{i}@example.com'
                    user = User.objects.create(
                        username=email,
                        email=email,
                        password=make_password('password'),
                        role='tutor'
                    )
                    spec = random.choice(all_subjects).subject_name
                    tutor = Tutor.objects.create(
                        user=user,
                        full_name=f'Tutor {i+existing_tutors_count+1}',
                        specialization=spec
                    )
                    all_tutors.append(tutor)
            else:
                all_tutors = list(Tutor.objects.all())

            # Sessions (Target 2000)
            existing_sessions_count = Session.objects.count()
            sessions_needed = max(0, 2000 - existing_sessions_count)
            
            if sessions_needed > 0:
                self.stdout.write(f'Creating {sessions_needed} sessions...')
                batch_size = 500
                sessions_batch = []
                
                for i in range(sessions_needed):
                    # Random date within +/- 60 days
                    days_delta = random.randint(-60, 60)
                    dt = timezone.now().date() + timedelta(days=days_delta)
                    tm = timezone.now().replace(hour=random.randint(8, 19), minute=0, second=0).time()
                    
                    status_choice = random.choice(['pending', 'approved', 'completed', 'declined'])
                    # If date is future, can't be completed
                    if dt > timezone.now().date() and status_choice == 'completed':
                        status_choice = 'approved'
                        
                    s = Session(
                        student=random.choice(all_students),
                        tutor=random.choice(all_tutors),
                        subject=random.choice(all_subjects),
                        session_date=dt,
                        session_time=tm,
                        status=status_choice,
                        notes=f'Auto-generated session {i}'
                    )
                    sessions_batch.append(s)
                    
                    if len(sessions_batch) >= batch_size:
                        Session.objects.bulk_create(sessions_batch)
                        sessions_batch = []
                        self.stdout.write(f'Created {i+1} sessions...')
                
                if sessions_batch:
                    Session.objects.bulk_create(sessions_batch)

