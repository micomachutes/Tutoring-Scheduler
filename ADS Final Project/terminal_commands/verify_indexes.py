"""
Verify and create performance indexes for database
Ensures all indexes from advanced_features.sql are in place
"""

import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from django.db import connection

def check_index_exists(cursor, table_name, index_name):
    """Check if an index exists on a table"""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.statistics 
        WHERE table_schema = DATABASE() 
        AND table_name = %s 
        AND index_name = %s
    """, (table_name, index_name))
    return cursor.fetchone()[0] > 0

def create_index_safe(cursor, sql_statement, index_name):
    """Safely create an index if it doesn't exist"""
    try:
        cursor.execute(sql_statement)
        print(f"✓ Created index: {index_name}")
        return True
    except Exception as e:
        if "Duplicate key name" in str(e) or "already exists" in str(e).lower():
            print(f"✓ Index already exists: {index_name}")
            return True
        else:
            print(f"✗ Error creating index {index_name}: {e}")
            return False

def main():
    cursor = connection.cursor()
    
    print("="*60)
    print("Verifying Performance Indexes")
    print("="*60)
    
    indexes_to_create = [
        # Sessions table indexes
        ("sessions", "idx_sessions_status", "CREATE INDEX idx_sessions_status ON sessions(status)"),
        ("sessions", "idx_sessions_date", "CREATE INDEX idx_sessions_date ON sessions(session_date)"),
        ("sessions", "idx_sessions_tutor_status", "CREATE INDEX idx_sessions_tutor_status ON sessions(tutor_id, status)"),
        ("sessions", "idx_sessions_student_status", "CREATE INDEX idx_sessions_student_status ON sessions(student_id, status)"),
        
        # Users table indexes
        ("users", "idx_users_email", "CREATE INDEX idx_users_email ON users(email)"),
        ("users", "idx_users_role", "CREATE INDEX idx_users_role ON users(role)"),
        
        # Tutors table indexes
        ("tutors", "idx_tutors_specialization", "CREATE INDEX idx_tutors_specialization ON tutors(specialization)"),
        
        # Subjects table indexes
        ("subjects", "idx_subjects_name", "CREATE INDEX idx_subjects_name ON subjects(subject_name)"),
    ]
    
    created_count = 0
    existing_count = 0
    
    for table_name, index_name, sql in indexes_to_create:
        if check_index_exists(cursor, table_name, index_name):
            print(f"✓ {index_name} already exists on {table_name}")
            existing_count += 1
        else:
            if create_index_safe(cursor, sql, index_name):
                created_count += 1
    
    print("\n" + "="*60)
    print(f"Summary: {created_count} new index(es) created, {existing_count} already exist")
    print("="*60)
    
    # Show all indexes
    print("\nAll Indexes by Table:")
    print("-"*60)
    
    tables = ['sessions', 'users', 'tutors', 'subjects', 'students']
    for table in tables:
        cursor.execute(f"SHOW INDEX FROM {table}")
        indexes = cursor.fetchall()
        if indexes:
            print(f"\n{table.upper()}:")
            for idx in indexes:
                idx_name = idx[2] if len(idx) > 2 else 'N/A'
                idx_col = idx[4] if len(idx) > 4 else 'N/A'
                print(f"  - {idx_name} on {idx_col}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

