# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Database
Edit `tutoring_system/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tutoringdb',
        'USER': 'root',
        'PASSWORD': '',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 3: Create Database & Run Migrations
```sql
CREATE DATABASE tutoringdb;
```

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Install Advanced SQL Features
```bash
mysql -u root -p tutoringdb < sql/advanced_features.sql
```

### Step 5: Populate Sample Data
```bash
python populate_data.py
```

### Step 6: Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Test Accounts
- Student: `student1@example.com` / `password`
- Tutor: `tutor1@example.com` / `password`

## Features Checklist
✅ Login/Logout (Student & Tutor)  
✅ Student: Create session requests  
✅ Student: View session status  
✅ Tutor: Accept/Decline requests  
✅ Session Log with filtering  
✅ Dashboard with charts  
✅ Advanced SQL features  

## Common Issues

**mysqlclient won't install?**
```bash
pip install pymysql
```
Then add to `tutoring_system/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

**Database connection error?**
- Check MySQL is running
- Verify database name and credentials
- Test connection: `mysql -u root -p`

**No data showing?**
- Run: `python populate_data.py`
- Check: Database has records in tables

