# SmartHire - Quick Setup Guide

## One-Click Setup

Simply double-click **`start_smarthire.bat`** to:
- Install all Python dependencies
- Set up MySQL database
- Create database tables
- Create test user accounts
- Start the application

## Prerequisites

Before running, ensure you have:

1. **Python 3.8+** installed and added to PATH
2. **XAMPP** (or MySQL) installed and running
   - MySQL service must be running
   - Default MySQL root user should have no password (or update scripts)

## Quick Start Files

### `start_smarthire.bat`
Complete setup and launch - use this the first time or after system changes.

### `run_smarthire.bat`
Quick start - use this when everything is already set up.

## Test Login Credentials

After running the setup, you can login with:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Applicant | `applicant1` | `applicant123` |
| Employer | `employer1` | `employer123` |

## Access the Application

Once started, open your browser and go to:
- http://localhost:5000
- http://127.0.0.1:5000

## Troubleshooting

### MySQL Connection Error
- Ensure XAMPP MySQL is running
- Check that MySQL service is started in XAMPP Control Panel
- Verify MySQL root user has no password (default XAMPP setup)

### Python Not Found
- Install Python 3.8+ from python.org
- Make sure Python is added to your system PATH
- Restart command prompt after installing Python

### Port 5000 Already in Use
- Close any other applications using port 5000
- Or modify `app.py` to use a different port

## Manual Setup (if batch file fails)

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install spaCy model:
   ```
   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
   ```

3. Setup database:
   ```
   python setup_database.py
   python init_db.py
   python create_test_users.py
   ```

4. Run application:
   ```
   python app.py
   ```

## Support

If you encounter any issues, check:
1. Python version: `python --version` (should be 3.8+)
2. MySQL is running in XAMPP
3. All dependencies are installed: `pip list`



