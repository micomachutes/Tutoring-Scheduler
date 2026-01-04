"""
Script to fix users table structure to match Django's AbstractUser requirements
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'database': 'tutoringdb',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'use_unicode': True
}

def check_column_exists(cursor, table, column):
    """Check if a column exists in a table"""
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'tutoringdb' 
        AND TABLE_NAME = '{table}' 
        AND COLUMN_NAME = '{column}'
    """)
    return cursor.fetchone()[0] > 0

def add_column_if_not_exists(cursor, table, column_def):
    """Add a column if it doesn't exist"""
    column_name = column_def.split()[0]
    if not check_column_exists(cursor, table, column_name):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")
            print(f"✓ Added column: {column_name}")
            return True
        except Error as e:
            print(f"✗ Error adding {column_name}: {e}")
            return False
    else:
        print(f"- Column {column_name} already exists")
        return True

def main():
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        print("Checking and fixing users table structure...")
        print("=" * 50)
        
        # Required Django AbstractUser fields
        columns_to_add = [
            "username VARCHAR(150) NOT NULL AFTER email",
            "first_name VARCHAR(150) DEFAULT ''",
            "last_name VARCHAR(150) DEFAULT ''",
            "is_staff TINYINT(1) DEFAULT 0",
            "is_active TINYINT(1) DEFAULT 1",
            "is_superuser TINYINT(1) DEFAULT 0",
            "last_login DATETIME NULL",
            "date_joined DATETIME DEFAULT CURRENT_TIMESTAMP"
        ]
        
        # Check if username exists, if not add it first
        if not check_column_exists(cursor, 'users', 'username'):
            print("Adding username column...")
            cursor.execute("ALTER TABLE users ADD COLUMN username VARCHAR(150) NULL AFTER email")
            connection.commit()
            
            # Update existing records
            print("Updating existing usernames...")
            cursor.execute("UPDATE users SET username = SUBSTRING_INDEX(email, '@', 1) WHERE username IS NULL")
            connection.commit()
            
            # Make it NOT NULL and add unique constraint
            print("Adding constraints to username...")
            cursor.execute("ALTER TABLE users MODIFY COLUMN username VARCHAR(150) NOT NULL")
            try:
                cursor.execute("ALTER TABLE users ADD UNIQUE KEY username_unique (username)")
            except Error as e:
                if 'Duplicate key' not in str(e):
                    print(f"Note: {e}")
            connection.commit()
            print("✓ Username column added and populated")
        else:
            print("- Username column already exists")
        
        # Add other columns
        for col_def in columns_to_add[1:]:  # Skip username, already handled
            add_column_if_not_exists(cursor, 'users', col_def)
        
        connection.commit()
        
        # Verify structure
        print("\n" + "=" * 50)
        print("Verifying table structure...")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print(f"\nUsers table now has {len(columns)} columns:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        print("\n✓ Users table structure fixed!")
        
    except Error as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

if __name__ == "__main__":
    main()

