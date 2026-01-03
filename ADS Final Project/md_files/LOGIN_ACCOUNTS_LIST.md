# Login Accounts - Ready to Use! 🔑

## ✅ Passwords Reset Successfully

All accounts below now have password: **`test123`**

---

## 👨‍🎓 STUDENT ACCOUNTS (with sessions)

Use these to login as a **student**:

| # | Name | Email | Sessions | Password |
|---|------|-------|----------|----------|
| 1 | Rose Gardner | `rose.gardner338@aol.com` | 7 | `test123` |
| 2 | Kevin Hamilton | `kevin.hamilton1422@student.edu` | 6 | `test123` |
| 3 | Jennifer Moreno | `jennifer.moreno78@icloud.com` | 6 | `test123` |
| 4 | Kimberly Ellis | `kimberlyellis1383@gmx.com` | 6 | `test123` |
| 5 | Joyce Marshall | `joyce.marshall.1468@college.edu` | 6 | `test123` |
| 6 | Emma Gardner | `emmagardner1211@icloud.com` | 6 | `test123` |
| 7 | Emma Schmidt | `emmaschmidt943@yahoo.com` | 5 | `test123` |
| 8 | Virginia Hall | `virginia552@outlook.com` | 5 | `test123` |
| 9 | Patricia Gardner | `patriciagardner360@college.edu` | 5 | `test123` |
| 10 | Judith Porter | `judith.porter.571@hotmail.com` | 5 | `test123` |

---

## 👨‍🏫 TUTOR ACCOUNTS (with sessions)

Use these to login as a **tutor**:

| # | Name | Email | Sessions | Password |
|---|------|-------|----------|----------|
| 1 | Douglas Nguyen | `prof.douglas.nguyen1900@student.edu` | 12 | `test123` |
| 2 | Betty Ford | `betty.ford1849@mail.com` | 12 | `test123` |
| 3 | Willie Arnold | `willie1883@yandex.com` | 11 | `test123` |
| 4 | Cynthia Daniels | `cynthiadaniels1729@yahoo.com` | 10 | `test123` |
| 5 | Sophia Medina | `prof.sophia.medina1850@mail.com` | 10 | `test123` |
| 6 | Alan Kelly | `alankelly1819@hotmail.com` | 10 | `test123` |
| 7 | Mary Robertson | `maryrobertson1660@yandex.com` | 9 | `test123` |
| 8 | Joyce Payne | `joyce.payne.1657@college.edu` | 9 | `test123` |
| 9 | Samantha Johnson | `samantha1989@zoho.com` | 9 | `test123` |
| 10 | Gerald Powell | `gerald.powell1699@ymail.com` | 9 | `test123` |

---

## 🚀 How to Login

### Step 1: Start the Server
```bash
python manage.py runserver
```

### Step 2: Go to Login Page
Open your browser and go to:
```
http://127.0.0.1:8000/login/
```

### Step 3: Enter Credentials
- **Email:** Use any email from the tables above
- **Password:** `test123`

### Step 4: Click Login
You should be redirected to the dashboard with data!

---

## 📊 What You'll See

### As a Student:
- **Dashboard** with YOUR session statistics
- **Session Log** showing YOUR sessions
- **Request Session** to create new requests

### As a Tutor:
- **Dashboard** with YOUR session statistics
- **Session Requests** showing sessions assigned to YOU
- **Session Log** showing YOUR sessions

---

## 🔐 Admin Account

To see ALL data (not just your own):

- **Username:** `machutesmicoadmin`
- **Email:** `machutesmico@admin.com`
- **Password:** `mM56252698`
- **URL:** `http://127.0.0.1:8000/admin/`

---

## ⚠️ Why Passwords Don't Work from phpMyAdmin

Django stores passwords as **hashed values**, not plain text. You cannot:
- ❌ See the actual password in phpMyAdmin
- ❌ Use the password field value directly
- ❌ Copy/paste from database

You can:
- ✅ Use the accounts above with password `test123`
- ✅ Reset passwords using Django shell
- ✅ Change passwords in Django admin

---

## 🔄 Reset More Passwords

If you need to reset passwords for other accounts:

```bash
python reset_passwords_for_login.py
```

Or manually in Django shell:
```bash
python manage.py shell
```

```python
from tutoring_app.models import User
user = User.objects.get(email='your-email@example.com')
user.set_password('newpassword')
user.save()
exit()
```

---

## ✅ Quick Test

**Recommended Test Account:**
- **Email:** `rose.gardner338@aol.com`
- **Password:** `test123`
- **Role:** Student
- **Sessions:** 7 (will show data!)

**Login and you should see:**
- Dashboard with statistics
- 7 sessions in the session log
- Charts and graphs with data

---

**All accounts above are ready to use! Just use password `test123` for any of them!** 🎉

