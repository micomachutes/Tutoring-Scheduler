how t-- =====================================================
-- Advanced SQL Features for Tutor Session Scheduler
-- =====================================================
-- This file contains: Triggers, Stored Functions, 
-- Stored Procedures, Views, Indexes, and Subqueries
-- =====================================================

USE tutoringdb;

-- =====================================================
-- 1. INDEXES (Performance Optimization)
-- =====================================================

-- Index on sessions table for status filtering
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);

-- Index on sessions table for date range queries
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date);

-- Composite index for tutor and status queries
CREATE INDEX IF NOT EXISTS idx_sessions_tutor_status ON sessions(tutor_id, status);

-- Composite index for student and status queries
CREATE INDEX IF NOT EXISTS idx_sessions_student_status ON sessions(student_id, status);

-- Index on users table for email lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index on users table for role filtering
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Index on tutors table for specialization searches
CREATE INDEX IF NOT EXISTS idx_tutors_specialization ON tutors(specialization);

-- Index on subjects table for name searches
CREATE INDEX IF NOT EXISTS idx_subjects_name ON subjects(subject_name);


-- =====================================================
-- 2. VIEWS (Data Abstraction)
-- =====================================================

-- View: Active Sessions Summary
-- Shows all active (pending/approved) sessions with student and tutor details
CREATE OR REPLACE VIEW v_active_sessions AS
SELECT 
    s.session_id,
    s.session_date,
    s.session_time,
    s.status,
    s.notes,
    s.created_at,
    st.full_name AS student_name,
    st.student_id,
    t.full_name AS tutor_name,
    t.tutor_id,
    t.specialization,
    sub.subject_name,
    sub.subject_id
FROM sessions s
INNER JOIN students st ON s.student_id = st.student_id
INNER JOIN tutors t ON s.tutor_id = t.tutor_id
INNER JOIN subjects sub ON s.subject_id = sub.subject_id
WHERE s.status IN ('pending', 'approved')
ORDER BY s.session_date, s.session_time;

-- View: Session Statistics by Tutor
-- Shows statistics for each tutor (total, pending, approved, completed, declined)
CREATE OR REPLACE VIEW v_tutor_statistics AS
SELECT 
    t.tutor_id,
    t.full_name AS tutor_name,
    t.specialization,
    COUNT(s.session_id) AS total_sessions,
    SUM(CASE WHEN s.status = 'pending' THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN s.status = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN s.status = 'declined' THEN 1 ELSE 0 END) AS declined_count
FROM tutors t
LEFT JOIN sessions s ON t.tutor_id = s.tutor_id
GROUP BY t.tutor_id, t.full_name, t.specialization;

-- View: Session Statistics by Student
-- Shows statistics for each student
CREATE OR REPLACE VIEW v_student_statistics AS
SELECT 
    st.student_id,
    st.full_name AS student_name,
    COUNT(s.session_id) AS total_sessions,
    SUM(CASE WHEN s.status = 'pending' THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN s.status = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN s.status = 'declined' THEN 1 ELSE 0 END) AS declined_count
FROM students st
LEFT JOIN sessions s ON st.student_id = s.student_id
GROUP BY st.student_id, st.full_name;

-- View: Monthly Session Report
-- Shows session counts grouped by month and status
CREATE OR REPLACE VIEW v_monthly_sessions AS
SELECT 
    DATE_FORMAT(session_date, '%Y-%m') AS month_year,
    status,
    COUNT(*) AS session_count
FROM sessions
GROUP BY DATE_FORMAT(session_date, '%Y-%m'), status
ORDER BY month_year DESC, status;


-- =====================================================
-- 3. STORED FUNCTIONS
-- =====================================================

-- Function: Get total sessions for a tutor
DELIMITER //
CREATE FUNCTION fn_get_tutor_total_sessions(p_tutor_id INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count
    FROM sessions
    WHERE tutor_id = p_tutor_id;
    RETURN v_count;
END //
DELIMITER ;

-- Function: Get total sessions for a student
DELIMITER //
CREATE FUNCTION fn_get_student_total_sessions(p_student_id INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count
    FROM sessions
    WHERE student_id = p_student_id;
    RETURN v_count;
END //
DELIMITER ;

-- Function: Get session completion rate for a tutor
DELIMITER //
CREATE FUNCTION fn_get_tutor_completion_rate(p_tutor_id INT)
RETURNS DECIMAL(5,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total INT;
    DECLARE v_completed INT;
    DECLARE v_rate DECIMAL(5,2);
    
    SELECT COUNT(*) INTO v_total
    FROM sessions
    WHERE tutor_id = p_tutor_id;
    
    IF v_total = 0 THEN
        RETURN 0.00;
    END IF;
    
    SELECT COUNT(*) INTO v_completed
    FROM sessions
    WHERE tutor_id = p_tutor_id AND status = 'completed';
    
    SET v_rate = (v_completed / v_total) * 100;
    RETURN v_rate;
END //
DELIMITER ;


-- =====================================================
-- 4. STORED PROCEDURES
-- =====================================================

-- Procedure: Get sessions by status for a tutor
DELIMITER //
CREATE PROCEDURE sp_get_tutor_sessions_by_status(
    IN p_tutor_id INT,
    IN p_status VARCHAR(10)
)
BEGIN
    SELECT 
        s.session_id,
        s.session_date,
        s.session_time,
        s.status,
        s.notes,
        st.full_name AS student_name,
        sub.subject_name
    FROM sessions s
    INNER JOIN students st ON s.student_id = st.student_id
    INNER JOIN subjects sub ON s.subject_id = sub.subject_id
    WHERE s.tutor_id = p_tutor_id
      AND (p_status IS NULL OR s.status = p_status)
    ORDER BY s.session_date, s.session_time;
END //
DELIMITER ;

-- Procedure: Get sessions by status for a student
DELIMITER //
CREATE PROCEDURE sp_get_student_sessions_by_status(
    IN p_student_id INT,
    IN p_status VARCHAR(10)
)
BEGIN
    SELECT 
        s.session_id,
        s.session_date,
        s.session_time,
        s.status,
        s.notes,
        t.full_name AS tutor_name,
        t.specialization,
        sub.subject_name
    FROM sessions s
    INNER JOIN tutors t ON s.tutor_id = t.tutor_id
    INNER JOIN subjects sub ON s.subject_id = sub.subject_id
    WHERE s.student_id = p_student_id
      AND (p_status IS NULL OR s.status = p_status)
    ORDER BY s.session_date, s.session_time;
END //
DELIMITER ;

-- Procedure: Update session status with validation
DELIMITER //
CREATE PROCEDURE sp_update_session_status(
    IN p_session_id INT,
    IN p_new_status VARCHAR(10),
    OUT p_result VARCHAR(100)
)
BEGIN
    DECLARE v_current_status VARCHAR(10);
    DECLARE v_valid_transition BOOLEAN DEFAULT FALSE;
    
    -- Get current status
    SELECT status INTO v_current_status
    FROM sessions
    WHERE session_id = p_session_id;
    
    -- Validate status transition
    IF v_current_status = 'pending' AND p_new_status IN ('approved', 'declined') THEN
        SET v_valid_transition = TRUE;
    ELSEIF v_current_status = 'approved' AND p_new_status = 'completed' THEN
        SET v_valid_transition = TRUE;
    END IF;
    
    IF v_valid_transition THEN
        UPDATE sessions
        SET status = p_new_status
        WHERE session_id = p_session_id;
        
        SET p_result = 'Status updated successfully';
    ELSE
        SET p_result = CONCAT('Invalid status transition from ', v_current_status, ' to ', p_new_status);
    END IF;
END //
DELIMITER ;


-- =====================================================
-- 5. TRIGGERS
-- =====================================================

-- Trigger: Log session status changes
-- Creates an audit trail when session status is updated
CREATE TABLE IF NOT EXISTS session_audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    old_status VARCHAR(10),
    new_status VARCHAR(10),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER trg_session_status_update
AFTER UPDATE ON sessions
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO session_audit_log (session_id, old_status, new_status)
        VALUES (NEW.session_id, OLD.status, NEW.status);
    END IF;
END //
DELIMITER ;

-- Trigger: Prevent duplicate sessions for same tutor/student/time
DELIMITER //
CREATE TRIGGER trg_prevent_duplicate_session
BEFORE INSERT ON sessions
FOR EACH ROW
BEGIN
    DECLARE v_count INT;
    
    SELECT COUNT(*) INTO v_count
    FROM sessions
    WHERE student_id = NEW.student_id
      AND tutor_id = NEW.tutor_id
      AND session_date = NEW.session_date
      AND session_time = NEW.session_time
      AND status IN ('pending', 'approved');
    
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A session already exists for this student, tutor, date, and time';
    END IF;
END //
DELIMITER ;

-- Trigger: Auto-update session to completed if date has passed
DELIMITER //
CREATE TRIGGER trg_auto_complete_past_sessions
BEFORE UPDATE ON sessions
FOR EACH ROW
BEGIN
    IF NEW.status = 'approved' 
       AND NEW.session_date < CURDATE() 
       AND OLD.status != 'completed' THEN
        SET NEW.status = 'completed';
    END IF;
END //
DELIMITER ;


-- =====================================================
-- 6. EXAMPLE QUERIES WITH SUBQUERIES
-- =====================================================

-- Query 1: Get tutors with above-average session counts
-- Uses subquery to calculate average and compare
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
ORDER BY session_count DESC;

-- Query 2: Get students who have more sessions than the average
SELECT 
    st.student_id,
    st.full_name,
    (SELECT COUNT(*) FROM sessions s WHERE s.student_id = st.student_id) AS session_count
FROM students st
WHERE (SELECT COUNT(*) FROM sessions s WHERE s.student_id = st.student_id) > 
      (SELECT AVG(student_session_count) 
       FROM (SELECT student_id, COUNT(*) AS student_session_count 
             FROM sessions GROUP BY student_id) AS avg_sessions)
ORDER BY session_count DESC;

-- Query 3: Get subjects with the most sessions (using subquery)
SELECT 
    sub.subject_id,
    sub.subject_name,
    (SELECT COUNT(*) FROM sessions s WHERE s.subject_id = sub.subject_id) AS total_sessions,
    (SELECT COUNT(*) FROM sessions s 
     WHERE s.subject_id = sub.subject_id AND s.status = 'completed') AS completed_sessions
FROM subjects sub
ORDER BY total_sessions DESC;

-- Query 4: Get tutors who have never declined a session
SELECT 
    t.tutor_id,
    t.full_name,
    t.specialization
FROM tutors t
WHERE t.tutor_id NOT IN (
    SELECT DISTINCT tutor_id 
    FROM sessions 
    WHERE status = 'declined'
);

-- Query 5: Get upcoming sessions for students with pending requests
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
ORDER BY s.session_date, s.session_time;


-- =====================================================
-- END OF ADVANCED FEATURES
-- =====================================================

