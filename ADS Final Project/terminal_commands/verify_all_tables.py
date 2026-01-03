import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from django.db import connection

def check_table_exists(cursor, table_name):
    """Check if a table exists in the database"""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = DATABASE() 
        AND table_name = %s
    """, (table_name,))
    return cursor.fetchone()[0] > 0

def main():
    cursor = connection.cursor()
    
    # All tables that should exist
    django_tables = [
        'django_content_type',
        'django_session',
        'django_admin_log',
        'django_migrations',
        'auth_permission',
        'auth_group',
        'auth_group_permissions',
    ]
    
    custom_tables = [
        'users',
        'students',
        'tutors',
        'subjects',
        'sessions',
        'users_groups',
        'users_user_permissions',
    ]
    
    print("Checking all required tables...\n")
    print("Django System Tables:")
    print("-" * 50)
    missing_django = []
    for table in django_tables:
        exists = check_table_exists(cursor, table)
        status = "✓" if exists else "✗"
        print(f"{status} {table}")
        if not exists:
            missing_django.append(table)
    
    print("\nCustom App Tables:")
    print("-" * 50)
    missing_custom = []
    for table in custom_tables:
        exists = check_table_exists(cursor, table)
        status = "✓" if exists else "✗"
        print(f"{status} {table}")
        if not exists:
            missing_custom.append(table)
    
    print("\n" + "=" * 50)
    if missing_django or missing_custom:
        print("MISSING TABLES FOUND:")
        if missing_django:
            print(f"  Django tables: {', '.join(missing_django)}")
        if missing_custom:
            print(f"  Custom tables: {', '.join(missing_custom)}")
        print("\nRun 'python create_all_django_tables.py' to create missing Django tables.")
        print("Run 'python manage.py migrate' to create missing custom app tables.")
    else:
        print("✓ All required tables exist!")
    print("=" * 50)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

