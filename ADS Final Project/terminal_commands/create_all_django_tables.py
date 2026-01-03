import os
import sys
import django

# Add parent directory to path so Django can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutoring_system.settings')
django.setup()

from django.db import connection
from django.core.management import sql

def check_table_exists(cursor, table_name):
    """Check if a table exists in the database"""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = DATABASE() 
        AND table_name = %s
    """, (table_name,))
    return cursor.fetchone()[0] > 0

def create_table_safe(cursor, sql_statement, table_name):
    """Safely create a table if it doesn't exist"""
    if not check_table_exists(cursor, table_name):
        try:
            cursor.execute(sql_statement)
            print(f"✓ Created table: {table_name}")
            return True
        except Exception as e:
            print(f"✗ Error creating {table_name}: {e}")
            return False
    else:
        print(f"✓ Table already exists: {table_name}")
        return True

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
    created_count = 0
    
    print("Checking and creating Django system tables...\n")
    
    # 1. django_content_type (must be created first as other tables reference it)
    if not check_table_exists(cursor, 'django_content_type'):
        cursor.execute("""
            CREATE TABLE `django_content_type` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `name` varchar(100) NOT NULL,
                `app_label` varchar(100) NOT NULL,
                `model` varchar(100) NOT NULL
            )
        """)
        cursor.execute("""
            ALTER TABLE `django_content_type` 
            ADD CONSTRAINT `django_content_type_app_label_model_76bd3d3b_uniq` 
            UNIQUE (`app_label`, `model`)
        """)
        print("✓ Created table: django_content_type")
        created_count += 1
    else:
        print("✓ Table already exists: django_content_type")
    
    # 2. django_session
    if not check_table_exists(cursor, 'django_session'):
        cursor.execute("""
            CREATE TABLE `django_session` (
                `session_key` varchar(40) NOT NULL PRIMARY KEY,
                `session_data` longtext NOT NULL,
                `expire_date` datetime(6) NOT NULL
            )
        """)
        create_index_safe(cursor, """
            CREATE INDEX `django_session_expire_date_a5c62663` 
            ON `django_session` (`expire_date`)
        """, "django_session_expire_date_a5c62663")
        print("✓ Created table: django_session")
        created_count += 1
    else:
        print("✓ Table already exists: django_session")
    
    # 3. auth_permission
    if not check_table_exists(cursor, 'auth_permission'):
        cursor.execute("""
            CREATE TABLE `auth_permission` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `name` varchar(50) NOT NULL,
                `content_type_id` integer NOT NULL,
                `codename` varchar(100) NOT NULL
            )
        """)
        cursor.execute("""
            ALTER TABLE `auth_permission` 
            ADD CONSTRAINT `auth_permission_content_type_id_codename_01ab375a_uniq` 
            UNIQUE (`content_type_id`, `codename`)
        """)
        cursor.execute("""
            ALTER TABLE `auth_permission` 
            ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` 
            FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
        """)
        print("✓ Created table: auth_permission")
        created_count += 1
    else:
        print("✓ Table already exists: auth_permission")
    
    # 4. auth_group
    if not check_table_exists(cursor, 'auth_group'):
        cursor.execute("""
            CREATE TABLE `auth_group` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `name` varchar(80) NOT NULL UNIQUE
            )
        """)
        print("✓ Created table: auth_group")
        created_count += 1
    else:
        print("✓ Table already exists: auth_group")
    
    # 5. auth_group_permissions
    if not check_table_exists(cursor, 'auth_group_permissions'):
        cursor.execute("""
            CREATE TABLE `auth_group_permissions` (
                `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `group_id` integer NOT NULL,
                `permission_id` integer NOT NULL
            )
        """)
        cursor.execute("""
            ALTER TABLE `auth_group_permissions` 
            ADD CONSTRAINT `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` 
            UNIQUE (`group_id`, `permission_id`)
        """)
        cursor.execute("""
            ALTER TABLE `auth_group_permissions` 
            ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` 
            FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
        """)
        cursor.execute("""
            ALTER TABLE `auth_group_permissions` 
            ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` 
            FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
        """)
        print("✓ Created table: auth_group_permissions")
        created_count += 1
    else:
        print("✓ Table already exists: auth_group_permissions")
    
    # 6. django_admin_log
    if not check_table_exists(cursor, 'django_admin_log'):
        cursor.execute("""
            CREATE TABLE `django_admin_log` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `action_time` datetime(6) NOT NULL,
                `object_id` longtext NULL,
                `object_repr` varchar(200) NOT NULL,
                `action_flag` smallint UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
                `change_message` longtext NOT NULL,
                `content_type_id` integer NULL,
                `user_id` bigint NOT NULL
            )
        """)
        cursor.execute("""
            ALTER TABLE `django_admin_log` 
            ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` 
            FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
        """)
        cursor.execute("""
            ALTER TABLE `django_admin_log` 
            ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` 
            FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
        """)
        print("✓ Created table: django_admin_log")
        created_count += 1
    else:
        print("✓ Table already exists: django_admin_log")
    
    # 7. django_migrations (tracks migration state)
    if not check_table_exists(cursor, 'django_migrations'):
        cursor.execute("""
            CREATE TABLE `django_migrations` (
                `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `app` varchar(255) NOT NULL,
                `name` varchar(255) NOT NULL,
                `applied` datetime(6) NOT NULL
            )
        """)
        print("✓ Created table: django_migrations")
        created_count += 1
    else:
        print("✓ Table already exists: django_migrations")
    
    # 8. users_groups (junction table for User-Group many-to-many)
    if not check_table_exists(cursor, 'users_groups'):
        # First check if users table exists
        if check_table_exists(cursor, 'users'):
            # The users table uses user_id (int) as primary key based on migration 0002
            cursor.execute("""
                CREATE TABLE `users_groups` (
                    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `user_id` int NOT NULL,
                    `group_id` integer NOT NULL
                )
            """)
            cursor.execute("""
                ALTER TABLE `users_groups` 
                ADD CONSTRAINT `users_groups_user_id_group_id_fc7788e8_uniq` 
                UNIQUE (`user_id`, `group_id`)
            """)
            cursor.execute("""
                ALTER TABLE `users_groups` 
                ADD CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` 
                FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
            """)
            cursor.execute("""
                ALTER TABLE `users_groups` 
                ADD CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` 
                FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
            """)
            print("✓ Created table: users_groups")
            created_count += 1
        else:
            print("⚠ Skipped users_groups (users table doesn't exist yet)")
    else:
        print("✓ Table already exists: users_groups")
    
    # 9. users_user_permissions (junction table for User-Permission many-to-many)
    if not check_table_exists(cursor, 'users_user_permissions'):
        # First check if users table exists
        if check_table_exists(cursor, 'users'):
            # The users table uses user_id (int) as primary key based on migration 0002
            cursor.execute("""
                CREATE TABLE `users_user_permissions` (
                    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `user_id` int NOT NULL,
                    `permission_id` integer NOT NULL
                )
            """)
            cursor.execute("""
                ALTER TABLE `users_user_permissions` 
                ADD CONSTRAINT `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` 
                UNIQUE (`user_id`, `permission_id`)
            """)
            cursor.execute("""
                ALTER TABLE `users_user_permissions` 
                ADD CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` 
                FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
            """)
            cursor.execute("""
                ALTER TABLE `users_user_permissions` 
                ADD CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` 
                FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
            """)
            print("✓ Created table: users_user_permissions")
            created_count += 1
        else:
            print("⚠ Skipped users_user_permissions (users table doesn't exist yet)")
    else:
        print("✓ Table already exists: users_user_permissions")
    
    print(f"\n{'='*50}")
    print(f"Summary: {created_count} new table(s) created")
    print(f"{'='*50}")
    print("\nAll Django system tables are now set up!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

