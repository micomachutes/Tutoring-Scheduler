# Django Admin - What You Should See (Visual Guide)

## Step-by-Step: What to Expect

### Step 1: Login to Admin
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with:
   - **Username:** `machutesmicoadmin`
   - **Password:** `mM56252698`

### Step 2: Admin Homepage

After logging in, you should see the **Django Administration** homepage with **TWO MAIN SECTIONS**:

---

## 📦 SECTION 1: TUTORING_APP

This section contains your application models. You should see:

```
┌─────────────────────────────────────────┐
│ TUTORING_APP                            │
├─────────────────────────────────────────┤
│ 👤 Users          (2,007)               │
│ 👨‍🎓 Students      (1,504)               │
│ 👨‍🏫 Tutors        (502)                 │
│ 📚 Subjects       (100)                 │
│ 📅 Sessions       (2,001)                │
└─────────────────────────────────────────┘
```

**The numbers in parentheses show the COUNT of records!**

---

## 📦 SECTION 2: AUTHENTICATION AND AUTHORIZATION

This is Django's built-in section:

```
┌─────────────────────────────────────────┐
│ AUTHENTICATION AND AUTHORIZATION        │
├─────────────────────────────────────────┤
│ 👥 Groups                                │
│ 👤 Users                                 │
└─────────────────────────────────────────┘
```

---

## 🖱️ Step 3: Click on Each Model

### When You Click "Users" (in TUTORING_APP section):

You should see a **LIST PAGE** with:

**At the top:**
- "Select user to change" (title)
- "2,007 users" (total count)
- Search box
- Filter sidebar on the right

**In the table:**
- Columns: ID, Email, Username, Role, Staff, Superuser, Created
- **50 users per page** (pagination at bottom)
- Each row is a user record

**Example rows you should see:**
```
ID | Email                          | Username        | Role    | ...
1  | abigail1@yandex.com           | abigailwatson1  | student | ...
2  | martha2@live.com              | marthamendoza2 | student | ...
3  | mark3@mail.com                | markpierce3     | student | ...
...
```

---

### When You Click "Students":

You should see:
- **Title:** "Select student to change"
- **Count:** "1,504 students"
- **Columns:** Student ID, Full Name, User, Email
- **50 students per page**

**Example rows:**
```
Student ID | Full Name        | User | Email
1          | Abigail Watson   | 1    | abigail1@yandex.com
2          | Martha Mendoza   | 2    | martha2@live.com
...
```

---

### When You Click "Tutors":

You should see:
- **Title:** "Select tutor to change"
- **Count:** "502 tutors"
- **Columns:** Tutor ID, Full Name, Specialization, User, Email
- **Filter by Specialization** (right sidebar)

**Example rows:**
```
Tutor ID | Full Name      | Specialization    | User  | Email
1        | Mary Owens     | Computer Science  | 1501  | mary.owens.1501@...
2        | Stephen Murray | Computer Science  | 1502  | stephen1502@...
...
```

---

### When You Click "Subjects":

You should see:
- **Title:** "Select subject to change"
- **Count:** "100 subjects"
- **Columns:** Subject Name, Subject ID

**Example rows:**
```
Subject Name          | Subject ID
Mathematics           | 1
Physics               | 2
Chemistry             | 3
...
```

---

### When You Click "Sessions":

You should see:
- **Title:** "Select session to change"
- **Count:** "2,001 sessions"
- **Columns:** Session ID, Student, Tutor, Subject, Date, Time, Status, Created
- **Filters:** Status, Date, Subject (right sidebar)
- **Date hierarchy** navigation at top

**Example rows:**
```
Session ID | Student        | Tutor         | Subject      | Date       | Status
1          | Abigail Watson | Mary Owens    | Mathematics  | 2026-01-12 | approved
2          | Martha Mendoza | Stephen Murray | Physics      | 2026-01-15 | pending
...
```

---

## ⚠️ If You Don't See Data

### Issue 1: Empty List Page

**Symptoms:** You see the list page but no rows

**Check:**
1. Look at the **top of the page** - does it say "X users" or "X students"?
2. If it shows a count but no list:
   - Check if you're on **page 2+** (look for pagination)
   - Click "← Previous" or go to page 1
   - Check if **filters are applied** (right sidebar) - clear them
3. Try **refreshing** the page (F5 or Ctrl+R)
4. Try **clearing browser cache** (Ctrl+Shift+Delete)

### Issue 2: Can't See the Sections

**Symptoms:** Admin homepage is blank or only shows "Authentication and Authorization"

**Solutions:**
1. Make sure `tutoring_app` is in `INSTALLED_APPS` in `settings.py`
2. Check if models are registered - run: `python troubleshoot_admin.py`
3. Restart the server: Stop (Ctrl+C) and run `python manage.py runserver` again

### Issue 3: Wrong Counts

**Symptoms:** Shows "0 users" or "0 students"

**Solutions:**
1. Verify data exists: `python view_data.py`
2. Check database connection in `settings.py`
3. Verify you're connected to the right database

---

## 🔍 Quick Diagnostic

Run this to check everything:
```bash
python troubleshoot_admin.py
```

This will tell you:
- ✅ If data exists
- ✅ If models are registered
- ✅ If superuser is active
- ✅ If data is accessible

---

## 📸 What the Admin Homepage Should Look Like

```
┌─────────────────────────────────────────────────────────────┐
│ Django administration                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Welcome, machutesmicoadmin.                                │
│  View site | Change password | Log out                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ TUTORING_APP                                        │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 👤 Users          (2,007)                          │   │
│  │ 👨‍🎓 Students      (1,504)                          │   │
│  │ 👨‍🏫 Tutors        (502)                            │   │
│  │ 📚 Subjects       (100)                             │   │
│  │ 📅 Sessions       (2,001)                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ AUTHENTICATION AND AUTHORIZATION                   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 👥 Groups                                          │   │
│  │ 👤 Users                                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Expected Behavior

1. **Homepage shows sections** with model names and counts
2. **Clicking a model** shows a list of records
3. **Each list shows 50 records per page** (with pagination)
4. **You can search** using the search box
5. **You can filter** using the right sidebar
6. **You can click a record** to view/edit details

---

## 🧪 Test Checklist

- [ ] Can login to `/admin/` with superuser
- [ ] See "TUTORING_APP" section on homepage
- [ ] See counts in parentheses (2,007 users, etc.)
- [ ] Can click "Users" and see list
- [ ] Can click "Students" and see list
- [ ] Can click "Tutors" and see list
- [ ] Can click "Subjects" and see list
- [ ] Can click "Sessions" and see list

If all checked ✅, admin is working correctly!

---

## 🆘 Still Not Working?

1. **Take a screenshot** of what you see
2. **Check browser console** (F12) for errors
3. **Try different browser** (Chrome, Firefox, Edge)
4. **Clear browser cache** completely
5. **Restart Django server**

Run diagnostic:
```bash
python troubleshoot_admin.py
```

This will help identify the exact issue!

