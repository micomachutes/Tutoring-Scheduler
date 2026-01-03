-- Add username column to users table
-- This is required by Django's AbstractUser model

USE tutoringdb;

-- Add username column if it doesn't exist
ALTER TABLE users 
ADD COLUMN username VARCHAR(150) NULL AFTER email;

-- Update existing records to use email as username (before unique constraint)
UPDATE users SET username = SUBSTRING_INDEX(email, '@', 1) WHERE username IS NULL;

-- Make username unique and not null
ALTER TABLE users 
MODIFY COLUMN username VARCHAR(150) NOT NULL;

-- Add unique constraint
ALTER TABLE users 
ADD UNIQUE KEY username (username);

-- Also add other Django AbstractUser required fields if missing
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS first_name VARCHAR(150) DEFAULT '',
ADD COLUMN IF NOT EXISTS last_name VARCHAR(150) DEFAULT '',
ADD COLUMN IF NOT EXISTS is_staff TINYINT(1) DEFAULT 0,
ADD COLUMN IF NOT EXISTS is_active TINYINT(1) DEFAULT 1,
ADD COLUMN IF NOT EXISTS is_superuser TINYINT(1) DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_login DATETIME NULL,
ADD COLUMN IF NOT EXISTS date_joined DATETIME DEFAULT CURRENT_TIMESTAMP;

