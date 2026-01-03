# Tutor Session Scheduler System

A comprehensive Django-based tutor session scheduling system with advanced SQL features, CRUD operations, and a modern GUI interface.

## Features

### User Authentication
- Login/Logout functionality
- Role-based access (Student, Tutor, Admin)
- Secure password hashing

### Student Features
- Create session requests (subject, date, time, optional notes)
- View session status (pending, approved, declined, completed)
- View session log with filtering
- Delete pending/declined sessions

### Tutor Features
- View incoming session requests
- Accept or decline session requests
- View all sessions (pending, approved, declined, completed)
- Filter sessions by status, subject, date range

### Dashboard
- Data visualization with charts
- Statistics (total, pending, approved, completed sessions)
- Sessions by subject (pie chart)
- Sessions by month (line chart)
- Upcoming sessions list

### Advanced SQL Features
- **Triggers**: 
  - Audit log for status changes
  - Prevent duplicate sessions
  - Auto-complete past sessions
- **Stored Functions**: 
  - Get tutor/student total sessions
  - Calculate completion rates
- **Stored Procedures**: 
  - Get sessions by status
  - Update session status with validation
- **Views**: 
  - Active sessions summary
  - Tutor/student statistics
  - Monthly session reports
- **Indexes**: 
  - Performance optimization on frequently queried columns
- **Subqueries**: 
  - Used in dashboard statistics and reports

## Project Structure

```
ADS Final Project/
├── tutoring_system/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tutoring_app/             # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # URL routing
│   ├── forms.py              # Django forms
│   └── admin.py              # Admin interface
├── templates/                # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── registration/
│   ├── student/
│   ├── tutor/
│   └── session_log.html
├── sql/                      # SQL scripts
│   ├── advanced_features.sql # Triggers, functions, procedures, views
│   └── populate_data.sql     # Data population script
├── populate_data.py          # Python data population script
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

## Database Schema

### Tables
1. **users** - User accounts with authentication
2. **students** - Student profiles
3. **tutors** - Tutor profiles with specialization
4. **subjects** - Available subjects
5. **sessions** - Tutoring session requests and records

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL/MariaDB
- Django 4.2+
- mysqlclient

### Step 1: Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE tutoringdb;
```

2. Run the provided SQL schema (if not using Django migrations):
```sql
USE tutoringdb;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'tutor', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE tutors (
    tutor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);

CREATE TABLE sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    tutor_id INT NOT NULL,
    subject_id INT NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    status ENUM('pending', 'approved', 'declined', 'completed') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);
```

3. Run advanced SQL features:
```bash
mysql -u root -p tutoringdb < sql/advanced_features.sql
```

### Step 2: Python Environment Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Update database settings in `tutoring_system/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tutoringdb',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 3: Django Setup

1. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create superuser (optional):
```bash
python manage.py createsuperuser
```

### Step 4: Populate Sample Data

Option 1: Using Python script (Recommended):
```bash
python populate_data.py
```

Option 2: Using SQL script:
```bash
mysql -u root -p tutoringdb < sql/populate_data.sql
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000`

## Usage

### Default Test Accounts

After running the data population script, you can login with:
- **Student**: `student1@example.com` / `password`
- **Tutor**: `tutor1@example.com` / `password`

### Student Workflow

1. Login as a student
2. Navigate to "Request Session"
3. Fill in subject, date, time, and optional notes
4. Submit request (status: pending)
5. View status in "Session Log"
6. Wait for tutor approval/decline

### Tutor Workflow

1. Login as a tutor
2. Navigate to "Session Requests"
3. View pending requests
4. Accept or decline requests
5. View all sessions in "Session Log"

## Advanced SQL Features Usage

### Using Stored Procedures

```sql
-- Get tutor sessions by status
CALL sp_get_tutor_sessions_by_status(1, 'pending');

-- Get student sessions by status
CALL sp_get_student_sessions_by_status(1, 'approved');

-- Update session status
CALL sp_update_session_status(1, 'approved', @result);
SELECT @result;
```

### Using Stored Functions

```sql
-- Get total sessions for a tutor
SELECT fn_get_tutor_total_sessions(1);

-- Get completion rate for a tutor
SELECT fn_get_tutor_completion_rate(1);
```

### Using Views

```sql
-- View active sessions
SELECT * FROM v_active_sessions;

-- View tutor statistics
SELECT * FROM v_tutor_statistics;

-- View monthly sessions
SELECT * FROM v_monthly_sessions;
```

## API Endpoints

The system uses Django views (not REST API), but the structure supports API implementation:

- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/dashboard/` - Dashboard with statistics
- `/student/create-session/` - Create session request
- `/tutor/requests/` - View session requests
- `/tutor/accept/<session_id>/` - Accept session
- `/tutor/decline/<session_id>/` - Decline session
- `/sessions/` - Session log with filtering
- `/sessions/complete/<session_id>/` - Mark session as completed
- `/sessions/delete/<session_id>/` - Delete session

## Technologies Used

- **Backend**: Django 4.2
- **Database**: MySQL/MariaDB
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: Django Authentication System

## Project Requirements Met

✅ **Individual Work**: Unique tutor session scheduler system  
✅ **CRUD Operations**: Full CRUD for users, students, tutors, subjects, sessions  
✅ **Advanced SQL Features**: 
   - ✅ Triggers (3 triggers)
   - ✅ Stored Functions (3 functions)
   - ✅ Stored Procedures (3 procedures)
   - ✅ Views (4 views)
   - ✅ Indexes (8 indexes)
   - ✅ Subqueries (used in views and queries)
✅ **GUI**: Modern, responsive interface with Bootstrap  
✅ **Input Validation**: Form validation and error handling  
✅ **Data Visualization**: Dashboard with charts  
✅ **Sample Data**: 1,500+ students, 500+ tutors, 2,000+ sessions  
✅ **Database**: MySQL with API-based access through Django ORM  

## Notes

- The system uses Django's ORM which provides an abstraction layer over SQL
- Advanced SQL features are implemented directly in the database
- All features serve functional purposes in the system
- The system is designed for local development (not deployed online)

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check database credentials in `settings.py`
- Ensure database `tutoringdb` exists

### Migration Issues
- Run `python manage.py migrate --run-syncdb` if needed
- Check for conflicting migrations

### Data Population Issues
- Ensure all tables exist before running population script
- Check MySQL user permissions

## License

This project is created for educational purposes as part of the ADS Final Project.

