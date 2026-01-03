import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from django.db import connection

try:
    cursor = connection.cursor()

    # Create the django_session table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `django_session` (
        `session_key` varchar(40) NOT NULL PRIMARY KEY,
        `session_data` longtext NOT NULL,
        `expire_date` datetime(6) NOT NULL
    )
    """)
    print("✓ Session table created or already exists")

    # Create the index
    try:
        cursor.execute("""
        CREATE INDEX `django_session_expire_date_a5c62663` 
        ON `django_session` (`expire_date`)
        """)
        print("✓ Index created successfully")
    except Exception as e:
        # Index might already exist
        if "Duplicate key name" in str(e) or "already exists" in str(e).lower():
            print("✓ Index already exists")
        else:
            print(f"Note: {e}")

    print("\nSession table setup completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

