# Realistic Data Update Guide

## Overview

The populate script has been updated to generate **realistic data** including:
- ✅ Real first and last names (from common name lists)
- ✅ Realistic email addresses (various formats and domains)
- ✅ Varied passwords (from a pool of common passwords)
- ✅ Realistic session notes (actual tutoring session descriptions)

---

## Option 1: Update Existing Data (Recommended)

If you already have data and want to update it to realistic values:

```bash
python update_to_realistic_data.py
```

This script will:
- Update all student names and emails to realistic values
- Update all tutor names and emails to realistic values
- Update session notes to realistic descriptions
- Preserve all existing relationships and IDs

**Note:** This modifies existing data. Make a backup if needed.

---

## Option 2: Clear and Repopulate

If you want to start fresh with realistic data:

### Step 1: Clear existing data (optional)
```sql
-- Connect to MySQL
mysql -u root -p tutoringdb

-- Clear data (be careful!)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE sessions;
TRUNCATE TABLE students;
TRUNCATE TABLE tutors;
TRUNCATE TABLE subjects;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;
```

### Step 2: Repopulate with realistic data
```bash
python populate_data.py
```

---

## View Sample Accounts

To see sample accounts with realistic data:

```bash
python show_sample_accounts.py
```

This shows:
- First 10 student accounts with names and emails
- First 10 tutor accounts with names, emails, and specializations
- Total counts

---

## What Changed

### Before (Generic Data)
- Names: `Student 1 Name`, `Tutor 1 Name`
- Emails: `student1@example.com`, `tutor1@example.com`
- Passwords: All `password`
- Notes: `Session notes for session 1`

### After (Realistic Data)
- Names: `James Smith`, `Mary Johnson`, `Robert Williams`
- Emails: `james.smith@gmail.com`, `mary.johnson@yahoo.com`, `robert.williams@student.edu`
- Passwords: Varied (`password123`, `Welcome123`, `Student2024`, etc.)
- Notes: `Need help with calculus homework on derivatives and integrals.`

---

## Email Format Examples

The script generates various email formats:
- `firstname.lastname@domain.com`
- `firstnamelastname@domain.com`
- `firstname123@domain.com`
- `firstname.lastname99@domain.com`
- `prof.firstname.lastname@domain.com` (for some tutors)

**Email Domains Used:**
- gmail.com, yahoo.com, hotmail.com, outlook.com
- student.edu, university.edu, college.edu
- And more...

---

## Password Information

Passwords are randomly selected from a pool of common passwords:
- `password123`, `Welcome123`, `Student2024`, `Tutor2024`
- `Learning123`, `Study2024`, `Education1`, etc.

**Note:** For production, users should change their passwords. These are for testing only.

---

## Session Notes Examples

Realistic session notes include:
- "Need help with calculus homework on derivatives and integrals."
- "Struggling with understanding database normalization concepts."
- "Review session for upcoming midterm exam in linear algebra."
- "Help with essay writing and thesis statement development."
- And 45+ more realistic variations

---

## Quick Start

1. **Update existing data:**
   ```bash
   python update_to_realistic_data.py
   ```

2. **View sample accounts:**
   ```bash
   python show_sample_accounts.py
   ```

3. **Test login:**
   - Check the sample accounts for email addresses
   - Use any password from the pool (or check database)
   - All passwords are hashed by Django

---

## Database Query to Find Accounts

To find accounts in the database:

```sql
-- Find student accounts
SELECT u.email, u.username, s.full_name 
FROM users u 
JOIN students s ON u.id = s.user_id 
LIMIT 10;

-- Find tutor accounts
SELECT u.email, u.username, t.full_name, t.specialization 
FROM users u 
JOIN tutors t ON u.id = t.user_id 
LIMIT 10;
```

---

## Files Created

1. **`populate_data.py`** - Updated to generate realistic data
2. **`update_to_realistic_data.py`** - Updates existing data to realistic values
3. **`show_sample_accounts.py`** - Shows sample accounts
4. **`REALISTIC_DATA_GUIDE.md`** - This guide

---

## Next Steps

1. ✅ Run `update_to_realistic_data.py` to update existing data
2. ✅ Run `show_sample_accounts.py` to view samples
3. ✅ Test login with realistic email addresses
4. ✅ Verify session notes are realistic

**Your database will now have realistic, professional-looking test data! 🎉**

