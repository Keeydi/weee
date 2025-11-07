#!/usr/bin/env python
"""
Initialize database tables for SmartHire
"""
from app import app, db

import sys

with app.app_context():
    print("=" * 60)
    print("Initializing SmartHire Database Tables")
    print("=" * 60)
    try:
        db.create_all()
        print("[SUCCESS] All database tables created successfully!")
        print("\nYou can now start the Flask application.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Failed to create tables: {e}")
        print("\nPlease ensure:")
        print("  1. MySQL/XAMPP is running")
        print("  2. Database 'smarthire' exists")
        print("  3. MySQL credentials are correct")
        sys.exit(1)

