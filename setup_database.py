#!/usr/bin/env python
"""
Database setup script for SmartHire
Creates the database if it doesn't exist and runs migrations
"""
import pymysql
from mysql.connector import Error
import sys

# Database configuration
HOST = "localhost"
USER = "root"
PASSWORD = ""  # Default XAMPP MySQL password
DATABASE = "smarthire"

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        conn = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"[OK] Database '{DATABASE}' is ready!")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"[ERROR] Error creating database: {e}")
        print("\n[WARNING] Please ensure:")
        print("   1. MySQL/XAMPP is running")
        print("   2. MySQL root user has no password (or update PASSWORD in this script)")
        print("   3. MySQL is accessible on localhost")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SmartHire Database Setup")
    print("=" * 60)
    
    if create_database():
        print("\n[SUCCESS] Database setup completed successfully!")
        print("   You can now run migrations with: flask db upgrade")
        sys.exit(0)
    else:
        print("\n[FAILED] Database setup failed!")
        sys.exit(1)

