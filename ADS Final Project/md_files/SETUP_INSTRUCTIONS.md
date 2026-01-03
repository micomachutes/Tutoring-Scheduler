# Setup Instructions

## Quick Start Guide

### 1. Prerequisites Installation

**Install Python 3.8+**
- Download from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**Install MySQL**
- Download MySQL from https://dev.mysql.com/downloads/mysql/
- Or use XAMPP which includes MySQL
- Make sure MySQL service is running

### 2. Database Setup

1. **Create the database:**
   ```sql
   CREATE DATABASE tutoringdb;
   ```

2. **Create tables using Django migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

   OR manually create tables using the SQL schema in README.md

3. **Run advanced SQL features:**
   ```bash
   mysql -u root -p tutoringdb < sql/advanced_features.sql
   ```

### 3. Python Environment Setup

1. **Navigate to project directory:**
   ```bash
   cd "C:\xampp\htdocs\ADS Final Project"
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If `mysqlclient` installation fails on Windows:
   - Download pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
   - Or use: `pip install pymysql` and update settings.py to use pymysql

### 4. Configure Database Settings

Edit `tutoring_system/settings.py` and update database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tutoringdb',
        'USER': 'root',
        'PASSWORD': '',  # Your MySQL password (empty if using XAMPP default)
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Populate Sample Data

**Option 1: Using Python script (Recommended)**
```bash
python populate_data.py
```

**Option 2: Using SQL script**
```bash
mysql -u root -p tutoringdb < sql/populate_data.sql
```

### 6. Run the Application

```bash
python manage.py runserver
```

Open your browser and navigate to: `http://127.0.0.1:8000`

### 7. Test Login

After populating data, you can login with:
- **Student**: `student1@example.com` / `password`
- **Tutor**: `tutor1@example.com` / `password`

## Troubleshooting

### Issue: mysqlclient installation fails

**Solution for Windows:**
1. Install MySQL Connector/C from MySQL website
2. Or use pymysql:
   ```bash
   pip install pymysql
   ```
   Then add to `tutoring_system/__init__.py`:
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### Issue: Database connection error

**Check:**
1. MySQL service is running
2. Database `tutoringdb` exists
3. Username and password in settings.py are correct
4. MySQL port is 3306 (default)

### Issue: Migration errors

**Solution:**
```bash
python manage.py migrate --run-syncdb
```

### Issue: Template not found

**Solution:**
- Make sure `templates` folder is in the project root
- Check `TEMPLATES` setting in `settings.py` includes the templates directory

### Issue: Static files not loading

**Solution:**
- The project uses CDN for Bootstrap and Chart.js, so no static files collection needed
- If you add custom static files, run: `python manage.py collectstatic`

## Alternative: Using SQL Server

If you need to use SQL Server instead of MySQL:

1. Install `pyodbc`:
   ```bash
   pip install pyodbc django-mssql-backend
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'sql_server.pyodbc',
           'NAME': 'tutoringdb',
           'USER': 'sa',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '1433',
           'OPTIONS': {
               'driver': 'ODBC Driver 17 for SQL Server',
           },
       }
   }
   ```

3. Update SQL syntax in `sql/advanced_features.sql` for SQL Server compatibility

## Project Structure Verification

After setup, your project should have:

```
ADS Final Project/
├── manage.py
├── requirements.txt
├── tutoring_system/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── tutoring_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── ...
├── sql/
│   ├── advanced_features.sql
│   └── populate_data.sql
└── populate_data.py
```

## Next Steps

1. ✅ Database created and tables migrated
2. ✅ Advanced SQL features installed
3. ✅ Sample data populated
4. ✅ Server running
5. ✅ Login and test the system

Enjoy your Tutor Session Scheduler System!

