"""
Production setup script for SmartHire.
Run this script on the server to configure production settings.
"""
import os
from app import app, db

def setup_production():
    """Set up production environment"""
    print("=" * 60)
    print("SmartHire Production Setup")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found!")
        print("Please create .env file from .env.example")
        print("and fill in your production credentials.")
        return
    
    # Create necessary directories
    directories = [
        'uploads',
        'resumes',
        'screened_resumes',
        'static/uploads',
        'static/screenings',
        'logs',
        'instance'
    ]
    
    print("\n📁 Creating necessary directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✓ Created: {directory}")
        else:
            print(f"   ✓ Exists: {directory}")
    
    # Initialize database
    print("\n🗄️  Initializing database...")
    try:
        with app.app_context():
            db.create_all()
            print("   ✓ Database tables created/verified")
    except Exception as e:
        print(f"   ✗ Error creating database: {e}")
        return
    
    # Check environment variables
    print("\n🔐 Checking environment variables...")
    required_vars = [
        'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME',
        'SECRET_KEY', 'MAIL_USERNAME', 'MAIL_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"   ⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("   Please update your .env file")
    else:
        print("   ✓ All required environment variables are set")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Make sure all environment variables are set in .env")
    print("2. Test the application: gunicorn -c gunicorn_config.py wsgi:app")
    print("3. Set up process manager (PM2 or Supervisor)")
    print("4. Configure your domain/subdomain")
    print("\n")

if __name__ == "__main__":
    setup_production()

