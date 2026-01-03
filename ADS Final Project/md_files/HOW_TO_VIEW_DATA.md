# How to Check Data in Django System

There are **5 main ways** to view your data in Django:

---

## Method 1: Django Admin Interface (Recommended) 🎯

The Django admin provides a web-based interface to view and manage all data.

### Step 1: Create a Superuser

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Username
- Email address
- Password

### Step 2: Start the Server

```bash
python manage.py runserver
```

### Step 3: Access Admin Panel

Open your browser and go to:
```
http://127.0.0.1:8000/admin/
```

Login with your superuser credentials.

### What You Can See:

- **Users** - All user accounts with email, username, role
- **Students** - Student profiles with full names
- **Tutors** - Tutor profiles with specializations
- **Subjects** - All available subjects
- **Sessions** - All tutoring sessions with filters and search

**Features:**
- ✅ Search by name, email, etc.
- ✅ Filter by status, date, role
- ✅ View detailed records
- ✅ Edit records (if needed)

---

## Method 2: Django Shell (Interactive) 💻

Access Django's interactive Python shell:

```bash
python manage.py shell
```

### Example Queries:

```python
# Import models
from tutoring_app.models import User, Student, Tutor, Subject, Session

# Count records
print(f"Total Users: {User.objects.count()}")
print(f"Total Students: {Student.objects.count()}")
print(f"Total Sessions: {Session.objects.count()}")

# View students
students = Student.objects.select_related('user').all()[:10]
for student in students:
    print(f"{student.full_name} - {student.user.email}")

# View sessions
sessions = Session.objects.select_related('student', 'tutor', 'subject').all()[:5]
for session in sessions:
    print(f"Session {session.session_id}: {session.student.full_name} with {session.tutor.full_name}")

# Filter sessions by status
pending = Session.objects.filter(status='pending').count()
approved = Session.objects.filter(status='approved').count()
print(f"Pending: {pending}, Approved: {approved}")

# Find user by email
user = User.objects.get(email='james.smith@gmail.com')
print(f"Found: {user.email}, Role: {user.role}")

# Exit shell
exit()
```

---

## Method 3: Quick View Script (Easiest) ⚡

Use the provided script to quickly view all data:

```bash
python view_data.py
```

This shows:
- Summary counts
- Sample students (first 10)
- Sample tutors (first 10)
- Sample sessions (first 10)
- Status breakdown
- All subjects

**Or use the sample accounts script:**

```bash
python show_sample_accounts.py
```

---

## Method 4: Web Application Interface 🌐

View data through the actual application:

### Step 1: Start Server

```bash
python manage.py runserver
```

### Step 2: Login

Go to: `http://127.0.0.1:8000/login/`

**To find login credentials:**
```bash
python show_sample_accounts.py
```

Or check in Django shell:
```python
from tutoring_app.models import User
User.objects.filter(role='student').first().email
```

### Step 3: Navigate Pages

- **Dashboard** (`/dashboard/`) - Statistics and charts
- **Session Log** (`/sessions/`) - All sessions with filtering
- **Student: Request Session** - Create new sessions
- **Tutor: Session Requests** - View and manage requests

---

## Method 5: Direct Database Queries (MySQL) 🗄️

Connect directly to MySQL:

```bash
mysql -u root -p tutoringdb
```

### Example Queries:

```sql
-- View all users
SELECT user_id, email, username, role FROM users LIMIT 10;

-- View students with emails
SELECT s.student_id, s.full_name, u.email 
FROM students s 
JOIN users u ON s.user_id = u.user_id 
LIMIT 10;

-- View tutors with emails
SELECT t.tutor_id, t.full_name, t.specialization, u.email 
FROM tutors t 
JOIN users u ON t.user_id = u.user_id 
LIMIT 10;

-- View sessions
SELECT s.session_id, st.full_name AS student, t.full_name AS tutor, 
       sub.subject_name, s.session_date, s.status
FROM sessions s
JOIN students st ON s.student_id = st.student_id
JOIN tutors t ON s.tutor_id = t.tutor_id
JOIN subjects sub ON s.subject_id = sub.subject_id
LIMIT 10;

-- Count by status
SELECT status, COUNT(*) as count 
FROM sessions 
GROUP BY status;

-- Find user by email
SELECT * FROM users WHERE email LIKE '%smith%';
```

---

## Quick Reference Commands

### View Data Summary
```bash
python view_data.py
```

### View Sample Accounts
```bash
python show_sample_accounts.py
```

### Django Shell
```bash
python manage.py shell
```

### Django Admin
```bash
python manage.py createsuperuser
python manage.py runserver
# Then visit: http://127.0.0.1:8000/admin/
```

### Database Direct Access
```bash
mysql -u root -p tutoringdb
```

---

## Recommended Workflow

1. **Quick Check**: Use `python view_data.py` for quick overview
2. **Detailed View**: Use Django Admin (`/admin/`) for full interface
3. **Data Analysis**: Use Django Shell for custom queries
4. **User Testing**: Use Web Application interface

---

## Tips

- **Django Admin** is best for browsing and managing data
- **Django Shell** is best for custom queries and data analysis
- **view_data.py** is best for quick summaries
- **Web Interface** is best for testing user experience

---

## Need Help?

If you can't see data:
1. Check if data exists: `python view_data.py`
2. Verify database connection
3. Check if migrations are applied: `python manage.py showmigrations`
4. Verify data population: `python populate_data.py`

