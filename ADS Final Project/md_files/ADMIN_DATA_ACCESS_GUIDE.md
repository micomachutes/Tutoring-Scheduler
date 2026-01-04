# How to Access Data in Django Admin - Step by Step

## ✅ Verification Complete

Your system has been verified:
- ✅ **2,005 Users** in database
- ✅ **1,503 Students** in database
- ✅ **501 Tutors** in database
- ✅ **100 Subjects** in database
- ✅ **2,000 Sessions** in database
- ✅ All models registered in admin
- ✅ Superuser created and active

---

## Step-by-Step: Accessing Data in Django Admin

### Step 1: Start the Django Server

Open terminal/command prompt and run:

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Open Django Admin

Open your web browser and go to:

```
http://127.0.0.1:8000/admin/
```

### Step 3: Login

Use these credentials:
- **Username:** `machutesmicoadmin`
- **Password:** `mM56252698`

### Step 4: Navigate to Data Sections

After logging in, you'll see the Django admin homepage with these sections:

#### **TUTORING_APP** Section:
1. **Users** - Click to see all 2,005 users
2. **Students** - Click to see all 1,503 students
3. **Tutors** - Click to see all 501 tutors
4. **Subjects** - Click to see all 100 subjects
5. **Sessions** - Click to see all 2,000 sessions

#### **AUTHENTICATION AND AUTHORIZATION** Section:
- **Groups** - Django groups
- **Users** - Same as above (Django's default user admin)

---

## What You Should See

### When You Click "Users":
- List of all users with columns: ID, Email, Username, Role, Staff, Superuser, Created
- **Total:** 2,005 users
- You can search by email or username
- You can filter by role, staff status, superuser status, or date

### When You Click "Students":
- List of all students with columns: Student ID, Full Name, User, Email
- **Total:** 1,503 students
- You can search by full name or email

### When You Click "Tutors":
- List of all tutors with columns: Tutor ID, Full Name, Specialization, User, Email
- **Total:** 501 tutors
- You can filter by specialization
- You can search by name or specialization

### When You Click "Subjects":
- List of all subjects with columns: Subject ID, Subject Name
- **Total:** 100 subjects
- You can search by subject name

### When You Click "Sessions":
- List of all sessions with columns: Session ID, Student, Tutor, Subject, Date, Time, Status
- **Total:** 2,000 sessions
- You can filter by status, date, or subject
- You can search by student name, tutor name, or subject name
- Date hierarchy navigation at the top

---

## Troubleshooting: If You Don't See Data

### Issue 1: Empty List Pages

**Symptoms:** You see the admin page but lists are empty

**Solutions:**
1. **Check the count at the top** - It should show "X users" or "X students"
2. **Scroll down** - Data might be on page 2 if paginated
3. **Check filters** - Make sure no filters are applied that hide data
4. **Clear browser cache** - Press Ctrl+F5 or clear cache
5. **Try incognito/private mode** - Rule out browser extensions

### Issue 2: Can't Login

**Symptoms:** Login page shows but can't authenticate

**Solutions:**
1. Verify credentials:
   - Username: `machutesmicoadmin`
   - Password: `mM56252698`
2. Check if superuser exists:
   ```bash
   python troubleshoot_admin.py
   ```
3. Reset password if needed:
   ```bash
   python create_superuser.py
   ```

### Issue 3: Models Not Showing

**Symptoms:** Admin page doesn't show Tutoring_App section

**Solutions:**
1. Check admin registration:
   ```bash
   python troubleshoot_admin.py
   ```
2. Restart the server:
   ```bash
   # Stop server (Ctrl+C)
   python manage.py runserver
   ```

### Issue 4: Server Won't Start

**Symptoms:** `python manage.py runserver` gives errors

**Solutions:**
1. Check if port 8000 is in use
2. Try different port:
   ```bash
   python manage.py runserver 8080
   ```
   Then access: `http://127.0.0.1:8080/admin/`
3. Check for Python/Django errors in terminal

---

## Quick Verification Commands

### Check Data Exists:
```bash
python view_data.py
```

### Check Admin Configuration:
```bash
python troubleshoot_admin.py
```

### View Sample Accounts:
```bash
python show_sample_accounts.py
```

---

## Alternative: View Data via Web Application

If admin still doesn't work, you can view data through the web app:

1. **Start server:**
   ```bash
   python manage.py runserver
   ```

2. **Login as student or tutor:**
   - Go to: `http://127.0.0.1:8000/login/`
   - Use any student/tutor account (check with `python show_sample_accounts.py`)

3. **View Dashboard:**
   - Shows statistics and charts
   - URL: `http://127.0.0.1:8000/dashboard/`

4. **View Session Log:**
   - Shows all sessions with filtering
   - URL: `http://127.0.0.1:8000/sessions/`

---

## Still Having Issues?

Run the troubleshooting script:
```bash
python troubleshoot_admin.py
```

This will show:
- ✅ Data counts
- ✅ Admin registration status
- ✅ Superuser status
- ✅ Data access tests
- ✅ Specific recommendations

---

## Expected Results

When everything works correctly, you should see:

- **Admin Homepage:** Lists all models with counts
- **Users Page:** 2,005 users listed
- **Students Page:** 1,503 students listed
- **Tutors Page:** 501 tutors listed
- **Subjects Page:** 100 subjects listed
- **Sessions Page:** 2,000 sessions listed

All pages should have:
- Search functionality
- Filter options
- Pagination (if many records)
- Clickable records to view details

---

**Your data is definitely in the database - the issue is likely with accessing it through the admin interface. Follow the steps above carefully!**

