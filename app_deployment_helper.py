"""
Helper code to update app.py for deployment platforms.
Copy the relevant section to your app.py file.
"""

# ============================================
# DATABASE CONFIGURATION FOR DEPLOYMENT
# ============================================
# Replace the database setup section in app.py (around line 29-33)
# with this code to support both MySQL and PostgreSQL

import os

# Get database URL from environment variable (platforms like Render/Railway provide this)
# Fallback to local MySQL for development
database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/smarthire')

# Convert postgres:// to postgresql:// if needed (SQLAlchemy requires postgresql://)
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ============================================
# GUNICORN CONFIGURATION FOR DEPLOYMENT
# ============================================
# Update gunicorn_config.py to use environment variable for port

# In gunicorn_config.py, change:
# bind = "127.0.0.1:8000"
# To:
import os
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# ============================================
# ENVIRONMENT VARIABLES TO SET
# ============================================
# Set these in your deployment platform's dashboard:

# Required:
# DATABASE_URL - Provided automatically by platform (Render, Railway, etc.)
# SECRET_KEY - Generate: python -c "import secrets; print(secrets.token_hex(32))"

# Optional (for email):
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-gmail-app-password
# MAIL_DEFAULT_SENDER=your-email@gmail.com

# ============================================
# SECRET KEY GENERATION
# ============================================
# Run this command to generate a secure secret key:
# python -c "import secrets; print(secrets.token_hex(32))"

