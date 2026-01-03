# Advanced SQL Features Implementation Guide

This document explains how all advanced SQL features are implemented in the Tutor Session Scheduler system and how to demonstrate them to your professor.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [1. INDEXES](#1-indexes)
3. [2. VIEWS](#2-views)
4. [3. STORED FUNCTIONS](#3-stored-functions)
5. [4. STORED PROCEDURES](#4-stored-procedures)
6. [5. TRIGGERS](#5-triggers)
6. [6. SUBQUERIES](#6-subqueries)
7. [Demonstration Guide](#demonstration-guide)

---

## Overview

All advanced SQL features are implemented in the file: **`sql/advanced_features.sql`**

**Location**: `sql/advanced_features.sql`

**Total Features Implemented**:
- ✅ **8 Indexes** - Performance optimization
- ✅ **4 Views** - Data abstraction and reporting
- ✅ **3 Stored Functions** - Reusable calculations
- ✅ **3 Stored Procedures** - Complex operations
- ✅ **3 Triggers** - Automated business logic
- ✅ **5 Example Subqueries** - Complex data retrieval

**All features serve functional purposes** in the tutoring system and are not isolated examples.

---

## 1. INDEXES

### Purpose
Indexes improve query performance by creating fast lookup paths for frequently queried columns.

### Implementation
**File**: `sql/advanced_features.sql` (Lines 10-36)

**8 Indexes Created**:

1. **`idx_sessions_status`** - Fast filtering by session status (pending/approved/completed/declined)
2. **`idx_sessions_date`** - Fast date range queries for sessions
3. **`idx_sessions_tutor_status`** - Composite index for tutor's sessions filtered by status
4. **`idx_sessions_student_status`** - Composite index for student's sessions filtered by status
5. **`idx_users_email`** - Fast email lookups during login
6. **`idx_users_role`** - Fast filtering by user role (student/tutor/admin)
7. **`idx_tutors_specialization`** - Fast searches for tutors by specialization
8. **`idx_subjects_name`** - Fast subject name searches

### How They're Used
- **Login system**: Uses `idx_users_email` to quickly find users by email
- **Dashboard**: Uses `idx_sessions_status` to count sessions by status
- **Session filtering**: Uses composite indexes for tutor/student session queries
- **Subject dropdown**: Uses `idx_subjects_name` for fast subject lookups

### Demonstration
```sql
-- Show all indexes
SHOW INDEX FROM sessions;
SHOW INDEX FROM users;
SHOW INDEX FROM tutors;

-- Check if indexes are being used (EXPLAIN shows index usage)
EXPLAIN SELECT * FROM sessions WHERE status = 'pending';
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

---

## 2. VIEWS

### Purpose
Views provide simplified, reusable query interfaces for complex joins and aggregations.

### Implementation
**File**: `sql/advanced_features.sql` (Lines 39-107)

**4 Views Created**:

#### 1. `v_active_sessions`
**Purpose**: Shows all active (pending/approved) sessions with full details
- Combines sessions, students, tutors, and subjects in one view
- Used for displaying upcoming sessions in the dashboard

#### 2. `v_tutor_statistics`
**Purpose**: Statistics for each tutor (total, pending, approved, completed, declined)
- Aggregates session counts by status for each tutor
- Used for tutor performance reports

#### 3. `v_student_statistics`
**Purpose**: Statistics for each student
- Aggregates session counts by status for each student
- Used for student activity reports

#### 4. `v_monthly_sessions`
**Purpose**: Monthly session reports grouped by month and status
- Used for generating monthly analytics and charts

### Demonstration
```sql
-- View active sessions
SELECT * FROM v_active_sessions LIMIT 10;

-- View tutor statistics
SELECT * FROM v_tutor_statistics ORDER BY total_sessions DESC LIMIT 10;

-- View student statistics
SELECT * FROM v_student_statistics ORDER BY total_sessions DESC LIMIT 10;

-- View monthly sessions
SELECT * FROM v_monthly_sessions ORDER BY month_year DESC;
```

---

## 3. STORED FUNCTIONS

### Purpose
Stored functions encapsulate reusable calculations that return a single value.

### Implementation
**File**: `sql/advanced_features.sql` (Lines 110-170)

**3 Functions Created**:

#### 1. `fn_get_tutor_total_sessions(p_tutor_id INT)`
**Returns**: Total number of sessions for a tutor
**Usage**: Calculate tutor workload

#### 2. `fn_get_student_total_sessions(p_student_id INT)`
**Returns**: Total number of sessions for a student
**Usage**: Track student activity

#### 3. `fn_get_tutor_completion_rate(p_tutor_id INT)`
**Returns**: Completion rate percentage (0.00 to 100.00)
**Usage**: Calculate tutor performance metrics

### Demonstration
```sql
-- Get total sessions for tutor ID 1
SELECT fn_get_tutor_total_sessions(1) AS tutor_sessions;

-- Get total sessions for student ID 1
SELECT fn_get_student_total_sessions(1) AS student_sessions;

-- Get completion rate for tutor ID 1
SELECT fn_get_tutor_completion_rate(1) AS completion_rate;

-- Use in a query
SELECT 
    tutor_id,
    full_name,
    fn_get_tutor_total_sessions(tutor_id) AS total_sessions,
    fn_get_tutor_completion_rate(tutor_id) AS completion_rate
FROM tutors
LIMIT 10;
```

---

## 4. STORED PROCEDURES

### Purpose
Stored procedures encapsulate complex operations with input/output parameters.

### Implementation
**File**: `sql/advanced_features.sql` (Lines 173-259)

**3 Procedures Created**:

#### 1. `sp_get_tutor_sessions_by_status(p_tutor_id INT, p_status VARCHAR(10))`
**Purpose**: Get all sessions for a tutor, optionally filtered by status
**Parameters**: 
- `p_tutor_id`: Tutor ID
- `p_status`: Status filter (NULL for all statuses)
**Returns**: Session list with student and subject details

#### 2. `sp_get_student_sessions_by_status(p_student_id INT, p_status VARCHAR(10))`
**Purpose**: Get all sessions for a student, optionally filtered by status
**Parameters**: 
- `p_student_id`: Student ID
- `p_status`: Status filter (NULL for all statuses)
**Returns**: Session list with tutor and subject details

#### 3. `sp_update_session_status(p_session_id INT, p_new_status VARCHAR(10), OUT p_result VARCHAR(100))`
**Purpose**: Update session status with validation
**Parameters**: 
- `p_session_id`: Session ID to update
- `p_new_status`: New status value
- `p_result`: Output parameter with result message
**Business Logic**: 
- Validates status transitions (pending → approved/declined, approved → completed)
- Prevents invalid transitions

### Demonstration
```sql
-- Get all pending sessions for tutor ID 1
CALL sp_get_tutor_sessions_by_status(1, 'pending');

-- Get all sessions for tutor ID 1 (all statuses)
CALL sp_get_tutor_sessions_by_status(1, NULL);

-- Get approved sessions for student ID 1
CALL sp_get_student_sessions_by_status(1, 'approved');

-- Update session status (valid transition)
CALL sp_update_session_status(1, 'approved', @result);
SELECT @result;

-- Try invalid transition (will return error message)
CALL sp_update_session_status(1, 'declined', @result);
SELECT @result;
```

---

## 5. TRIGGERS

### Purpose
Triggers automatically execute SQL code when specific database events occur.

### Implementation
**File**: `sql/advanced_features.sql` (Lines 262-324)

**3 Triggers Created**:

#### 1. `trg_session_status_update` (AFTER UPDATE)
**Purpose**: Audit log for session status changes
**When**: After updating a session's status
**Action**: 
- Creates entry in `session_audit_log` table
- Records old status, new status, and timestamp
- **Business Value**: Track all status changes for accountability

#### 2. `trg_prevent_duplicate_session` (BEFORE INSERT)
**Purpose**: Prevent duplicate sessions
**When**: Before inserting a new session
**Action**: 
- Checks if a session already exists for same student, tutor, date, and time
- Prevents insertion if duplicate found
- **Business Value**: Data integrity - prevents double-booking

#### 3. `trg_auto_complete_past_sessions` (BEFORE UPDATE)
**Purpose**: Auto-complete past approved sessions
**When**: Before updating a session
**Action**: 
- If session is approved and date has passed, automatically set status to 'completed'
- **Business Value**: Automatic status management

### Demonstration

#### Test Trigger 1: Audit Log
```sql
-- View current audit log
SELECT * FROM session_audit_log ORDER BY changed_at DESC LIMIT 10;

-- Update a session status (trigger will fire)
UPDATE sessions SET status = 'approved' WHERE session_id = 1 AND status = 'pending';

-- Check audit log (new entry should appear)
SELECT * FROM session_audit_log ORDER BY changed_at DESC LIMIT 5;
```

#### Test Trigger 2: Prevent Duplicates
```sql
-- Try to create duplicate session (should fail)
INSERT INTO sessions (student_id, tutor_id, subject_id, session_date, session_time, status)
VALUES (1, 1, 1, '2026-01-15', '10:00:00', 'pending');

-- Error message: "A session already exists for this student, tutor, date, and time"
```

#### Test Trigger 3: Auto-Complete
```sql
-- Create a past session
INSERT INTO sessions (student_id, tutor_id, subject_id, session_date, session_time, status)
VALUES (1, 1, 1, '2025-01-01', '10:00:00', 'approved');

-- Update the session (trigger will auto-complete it)
UPDATE sessions SET status = 'approved' WHERE session_id = LAST_INSERT_ID();

-- Check status (should be 'completed')
SELECT session_id, session_date, status FROM sessions WHERE session_id = LAST_INSERT_ID();
```

---

## 6. SUBQUERIES

### Purpose
Subqueries allow complex data retrieval by nesting queries within queries.

### Implementation
**File**: `sql/advanced_features.sql` (Lines 327-398)

**5 Example Queries with Subqueries**:

#### Query 1: Tutors with Above-Average Session Counts
**Purpose**: Find high-performing tutors
**Subquery Type**: Scalar subquery, correlated subquery

#### Query 2: Students with Above-Average Session Counts
**Purpose**: Find active students
**Subquery Type**: Scalar subquery, correlated subquery

#### Query 3: Subjects with Session Statistics
**Purpose**: Subject popularity analysis
**Subquery Type**: Scalar subquery (multiple)

#### Query 4: Tutors Who Never Declined
**Purpose**: Find most reliable tutors
**Subquery Type**: NOT IN subquery

#### Query 5: Upcoming Sessions for Students with Pending Requests
**Purpose**: Find students with both pending and approved sessions
**Subquery Type**: IN subquery

### Demonstration
```sql
-- Query 1: Tutors with above-average sessions
SELECT 
    t.tutor_id,
    t.full_name,
    t.specialization,
    (SELECT COUNT(*) FROM sessions s WHERE s.tutor_id = t.tutor_id) AS session_count
FROM tutors t
WHERE (SELECT COUNT(*) FROM sessions s WHERE s.tutor_id = t.tutor_id) > 
      (SELECT AVG(tutor_session_count) 
       FROM (SELECT tutor_id, COUNT(*) AS tutor_session_count 
             FROM sessions GROUP BY tutor_id) AS avg_sessions)
ORDER BY session_count DESC
LIMIT 10;

-- Query 2: Students with above-average sessions
SELECT 
    st.student_id,
    st.full_name,
    (SELECT COUNT(*) FROM sessions s WHERE s.student_id = st.student_id) AS session_count
FROM students st
WHERE (SELECT COUNT(*) FROM sessions s WHERE s.student_id = st.student_id) > 
      (SELECT AVG(student_session_count) 
       FROM (SELECT student_id, COUNT(*) AS student_session_count 
             FROM sessions GROUP BY student_id) AS avg_sessions)
ORDER BY session_count DESC
LIMIT 10;

-- Query 3: Subjects with most sessions
SELECT 
    sub.subject_id,
    sub.subject_name,
    (SELECT COUNT(*) FROM sessions s WHERE s.subject_id = sub.subject_id) AS total_sessions,
    (SELECT COUNT(*) FROM sessions s 
     WHERE s.subject_id = sub.subject_id AND s.status = 'completed') AS completed_sessions
FROM subjects sub
ORDER BY total_sessions DESC
LIMIT 10;

-- Query 4: Tutors who never declined
SELECT 
    t.tutor_id,
    t.full_name,
    t.specialization
FROM tutors t
WHERE t.tutor_id NOT IN (
    SELECT DISTINCT tutor_id 
    FROM sessions 
    WHERE status = 'declined'
)
LIMIT 10;

-- Query 5: Upcoming sessions for students with pending requests
SELECT 
    s.session_id,
    s.session_date,
    s.session_time,
    st.full_name AS student_name,
    t.full_name AS tutor_name,
    sub.subject_name
FROM sessions s
INNER JOIN students st ON s.student_id = st.student_id
INNER JOIN tutors t ON s.tutor_id = t.tutor_id
INNER JOIN subjects sub ON s.subject_id = sub.subject_id
WHERE s.status = 'approved'
  AND s.session_date >= CURDATE()
  AND s.student_id IN (
      SELECT student_id 
      FROM sessions 
      WHERE status = 'pending'
  )
ORDER BY s.session_date, s.session_time
LIMIT 10;
```

---

## Demonstration Guide

### Step 1: Verify All Features Are Installed

```bash
# Connect to MySQL
mysql -u root -p tutoringdb

# Check indexes
SHOW INDEX FROM sessions;
SHOW INDEX FROM users;
SHOW INDEX FROM tutors;

# Check views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

# Check stored functions
SHOW FUNCTION STATUS WHERE Db = 'tutoringdb';

# Check stored procedures
SHOW PROCEDURE STATUS WHERE Db = 'tutoringdb';

# Check triggers
SHOW TRIGGERS;
```

### Step 2: Demonstrate Each Feature

#### A. INDEXES
```sql
-- Show index usage in query execution
EXPLAIN SELECT * FROM sessions WHERE status = 'pending';
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

#### B. VIEWS
```sql
-- Show all views
SELECT * FROM v_active_sessions LIMIT 5;
SELECT * FROM v_tutor_statistics ORDER BY total_sessions DESC LIMIT 5;
SELECT * FROM v_student_statistics ORDER BY total_sessions DESC LIMIT 5;
SELECT * FROM v_monthly_sessions ORDER BY month_year DESC;
```

#### C. STORED FUNCTIONS
```sql
-- Test each function
SELECT fn_get_tutor_total_sessions(1);
SELECT fn_get_student_total_sessions(1);
SELECT fn_get_tutor_completion_rate(1);

-- Use in SELECT statement
SELECT 
    tutor_id,
    full_name,
    fn_get_tutor_total_sessions(tutor_id) AS sessions,
    fn_get_tutor_completion_rate(tutor_id) AS completion_rate
FROM tutors
LIMIT 5;
```

#### D. STORED PROCEDURES
```sql
-- Test procedures
CALL sp_get_tutor_sessions_by_status(1, 'pending');
CALL sp_get_student_sessions_by_status(1, 'approved');
CALL sp_update_session_status(1, 'approved', @result);
SELECT @result;
```

#### E. TRIGGERS
```sql
-- Test audit log trigger
SELECT * FROM session_audit_log ORDER BY changed_at DESC LIMIT 5;
UPDATE sessions SET status = 'approved' WHERE session_id = 1 AND status = 'pending';
SELECT * FROM session_audit_log ORDER BY changed_at DESC LIMIT 5;

-- Test duplicate prevention trigger (should fail)
INSERT INTO sessions (student_id, tutor_id, subject_id, session_date, session_time, status)
SELECT student_id, tutor_id, subject_id, session_date, session_time, status
FROM sessions LIMIT 1;
```

#### F. SUBQUERIES
```sql
-- Run example subquery queries (see section 6 above)
```

### Step 3: Show Integration with Django

1. **Start Django server**: `python manage.py runserver`
2. **Login as tutor/student**
3. **Show that triggers fire automatically**:
   - Create a session (trigger prevents duplicates)
   - Update session status (trigger creates audit log)
4. **Show that indexes improve performance**:
   - Dashboard loads quickly (uses indexed queries)
   - Session filtering is fast (uses composite indexes)

### Step 4: Create a Demonstration Script

Create a file `demonstrate_features.sql` with all the demonstration queries above, then run:

```bash
mysql -u root -p tutoringdb < demonstrate_features.sql
```

---

## Summary Checklist for Professor

✅ **INDEXES**: 8 indexes created and verified
- Show with `SHOW INDEX FROM table_name`
- Demonstrate with `EXPLAIN` queries

✅ **VIEWS**: 4 views created and functional
- Show with `SELECT * FROM view_name`
- Explain business purpose of each view

✅ **STORED FUNCTIONS**: 3 functions created
- Show with `SELECT fn_name(parameter)`
- Demonstrate in SELECT statements

✅ **STORED PROCEDURES**: 3 procedures created
- Show with `CALL procedure_name(...)`
- Demonstrate input/output parameters

✅ **TRIGGERS**: 3 triggers created and tested
- Show trigger execution with UPDATE/INSERT
- Show audit log table contents
- Demonstrate duplicate prevention

✅ **SUBQUERIES**: 5 example queries with subqueries
- Show complex nested queries
- Explain subquery types (scalar, correlated, IN, NOT IN)

---

## Files to Show Professor

1. **`sql/advanced_features.sql`** - Complete implementation file
2. **`ADVANCED_SQL_FEATURES_GUIDE.md`** - This documentation
3. **Database**: Live database with all features installed and working

---

## Quick Reference Commands

```sql
-- View all features
SHOW INDEX FROM sessions;
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SHOW FUNCTION STATUS WHERE Db = 'tutoringdb';
SHOW PROCEDURE STATUS WHERE Db = 'tutoringdb';
SHOW TRIGGERS;

-- Test features
SELECT * FROM v_active_sessions LIMIT 5;
SELECT fn_get_tutor_total_sessions(1);
CALL sp_get_tutor_sessions_by_status(1, 'pending');
SELECT * FROM session_audit_log ORDER BY changed_at DESC LIMIT 5;
```

---

**All features are functional and integrated into the system!** 🎉

