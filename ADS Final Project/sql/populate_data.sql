-- =====================================================
-- Data Population Script
-- Generates 1,000-2,000 records per table for testing
-- =====================================================

USE tutoringdb;

-- Clear existing data (optional - use with caution)
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE sessions;
-- TRUNCATE TABLE students;
-- TRUNCATE TABLE tutors;
-- TRUNCATE TABLE subjects;
-- TRUNCATE TABLE users;
-- SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- 1. POPULATE SUBJECTS (50 subjects)
-- =====================================================

INSERT INTO subjects (subject_name) VALUES
('Mathematics'), ('Physics'), ('Chemistry'), ('Biology'), ('English'),
('History'), ('Geography'), ('Computer Science'), ('Programming'), ('Data Structures'),
('Algorithms'), ('Database Systems'), ('Web Development'), ('Software Engineering'), ('Statistics'),
('Calculus'), ('Linear Algebra'), ('Discrete Mathematics'), ('Operating Systems'), ('Networks'),
('Machine Learning'), ('Artificial Intelligence'), ('Data Science'), ('Cybersecurity'), ('Mobile Development'),
('Spanish'), ('French'), ('German'), ('Chinese'), ('Japanese'),
('Economics'), ('Business Management'), ('Accounting'), ('Finance'), ('Marketing'),
('Psychology'), ('Sociology'), ('Philosophy'), ('Literature'), ('Art History'),
('Music Theory'), ('Physical Education'), ('Health Sciences'), ('Nursing'), ('Medicine'),
('Law'), ('Political Science'), ('International Relations'), ('Anthropology'), ('Archaeology');

-- =====================================================
-- 2. POPULATE USERS AND STUDENTS (1,500 students)
-- =====================================================

-- Generate 1,500 student users
SET @student_counter = 1;
WHILE @student_counter <= 1500 DO
    INSERT INTO users (email, password_hash, role, created_at)
    VALUES (
        CONCAT('student', @student_counter, '@example.com'),
        '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', -- password: password
        'student',
        DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY)
    );
    
    SET @user_id = LAST_INSERT_ID();
    
    INSERT INTO students (user_id, full_name)
    VALUES (
        @user_id,
        CONCAT('Student ', @student_counter, ' Name')
    );
    
    SET @student_counter = @student_counter + 1;
END WHILE;

-- =====================================================
-- 3. POPULATE USERS AND TUTORS (500 tutors)
-- =====================================================

-- Generate 500 tutor users
SET @tutor_counter = 1;
SET @specializations = 'Mathematics,Physics,Chemistry,Biology,English,Computer Science,Programming,Statistics,Calculus,Data Science';
SET @specialization_count = 10;

WHILE @tutor_counter <= 500 DO
    INSERT INTO users (email, password_hash, role, created_at)
    VALUES (
        CONCAT('tutor', @tutor_counter, '@example.com'),
        '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', -- password: password
        'tutor',
        DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY)
    );
    
    SET @user_id = LAST_INSERT_ID();
    
    -- Assign random specialization
    SET @rand_spec = FLOOR(RAND() * @specialization_count) + 1;
    SET @specialization = CASE @rand_spec
        WHEN 1 THEN 'Mathematics'
        WHEN 2 THEN 'Physics'
        WHEN 3 THEN 'Chemistry'
        WHEN 4 THEN 'Biology'
        WHEN 5 THEN 'English'
        WHEN 6 THEN 'Computer Science'
        WHEN 7 THEN 'Programming'
        WHEN 8 THEN 'Statistics'
        WHEN 9 THEN 'Calculus'
        ELSE 'Data Science'
    END;
    
    INSERT INTO tutors (user_id, full_name, specialization)
    VALUES (
        @user_id,
        CONCAT('Tutor ', @tutor_counter, ' Name'),
        @specialization
    );
    
    SET @tutor_counter = @tutor_counter + 1;
END WHILE;

-- =====================================================
-- 4. POPULATE SESSIONS (2,000 sessions)
-- =====================================================

-- Generate 2,000 sessions
SET @session_counter = 1;
SET @statuses = 'pending,approved,declined,completed';
SET @min_student_id = (SELECT MIN(student_id) FROM students);
SET @max_student_id = (SELECT MAX(student_id) FROM students);
SET @min_tutor_id = (SELECT MIN(tutor_id) FROM tutors);
SET @max_tutor_id = (SELECT MAX(tutor_id) FROM tutors);
SET @min_subject_id = (SELECT MIN(subject_id) FROM subjects);
SET @max_subject_id = (SELECT MAX(subject_id) FROM subjects);

WHILE @session_counter <= 2000 DO
    -- Random student, tutor, and subject
    SET @rand_student = @min_student_id + FLOOR(RAND() * (@max_student_id - @min_student_id + 1));
    SET @rand_tutor = @min_tutor_id + FLOOR(RAND() * (@max_tutor_id - @min_tutor_id + 1));
    SET @rand_subject = @min_subject_id + FLOOR(RAND() * (@max_subject_id - @min_subject_id + 1));
    
    -- Random date (between 30 days ago and 60 days in the future)
    SET @rand_date = DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 90 - 30) DAY);
    
    -- Random time (between 8 AM and 8 PM)
    SET @rand_hour = 8 + FLOOR(RAND() * 12);
    SET @rand_minute = FLOOR(RAND() * 4) * 15; -- 0, 15, 30, or 45
    SET @rand_time = CONCAT(LPAD(@rand_hour, 2, '0'), ':', LPAD(@rand_minute, 2, '0'), ':00');
    
    -- Random status (weighted: more pending and approved)
    SET @rand_status_num = FLOOR(RAND() * 100);
    SET @rand_status = CASE
        WHEN @rand_status_num < 30 THEN 'pending'
        WHEN @rand_status_num < 60 THEN 'approved'
        WHEN @rand_status_num < 80 THEN 'completed'
        ELSE 'declined'
    END;
    
    -- Random notes (50% chance)
    SET @rand_notes = CASE
        WHEN RAND() < 0.5 THEN CONCAT('Session notes for session ', @session_counter)
        ELSE NULL
    END;
    
    INSERT INTO sessions (
        student_id, tutor_id, subject_id, 
        session_date, session_time, status, notes, created_at
    )
    VALUES (
        @rand_student,
        @rand_tutor,
        @rand_subject,
        @rand_date,
        @rand_time,
        @rand_status,
        @rand_notes,
        DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 60) DAY)
    );
    
    SET @session_counter = @session_counter + 1;
END WHILE;

-- =====================================================
-- ALTERNATIVE: Using INSERT statements for MySQL compatibility
-- =====================================================

-- If the WHILE loop doesn't work, use this approach instead
-- This creates sample data using INSERT statements

-- Note: The WHILE loop approach above may not work in all MySQL versions
-- If you encounter issues, you can use a Python script to generate the data
-- or manually create batches of INSERT statements

-- Example batch insert for sessions (you would need to generate more):
/*
INSERT INTO sessions (student_id, tutor_id, subject_id, session_date, session_time, status, notes, created_at)
SELECT 
    (SELECT student_id FROM students ORDER BY RAND() LIMIT 1),
    (SELECT tutor_id FROM tutors ORDER BY RAND() LIMIT 1),
    (SELECT subject_id FROM subjects ORDER BY RAND() LIMIT 1),
    DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 90 - 30) DAY),
    SEC_TO_TIME(FLOOR(RAND() * 43200) + 28800), -- Random time between 8 AM and 8 PM
    ELT(FLOOR(RAND() * 4) + 1, 'pending', 'approved', 'completed', 'declined'),
    CASE WHEN RAND() < 0.5 THEN CONCAT('Notes for session ', @session_counter) ELSE NULL END,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 60) DAY)
FROM (SELECT @session_counter := 0) AS init
CROSS JOIN (
    SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION
    SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
) AS numbers
LIMIT 2000;
*/

-- =====================================================
-- END OF DATA POPULATION
-- =====================================================

-- Verify data counts
SELECT 'Users' AS table_name, COUNT(*) AS record_count FROM users
UNION ALL
SELECT 'Students', COUNT(*) FROM students
UNION ALL
SELECT 'Tutors', COUNT(*) FROM tutors
UNION ALL
SELECT 'Subjects', COUNT(*) FROM subjects
UNION ALL
SELECT 'Sessions', COUNT(*) FROM sessions;

