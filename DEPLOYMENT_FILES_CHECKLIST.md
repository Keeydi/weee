# Deployment Files Checklist

Use this checklist to ensure you have all necessary files before deploying to Hostinger.

## ✅ Required Files (Must Upload)

### Core Application Files
- [ ] `app.py` - Main Flask application
- [ ] `wsgi.py` - WSGI entry point (created for you)
- [ ] `gunicorn_config.py` - Gunicorn configuration (created for you)
- [ ] `requirements.txt` - Python dependencies
- [ ] `db_connector.py` - Database connector (if used)

### Templates (entire folder)
- [ ] `templates/` folder with all HTML files:
  - [ ] `base.html`
  - [ ] `index.html`
  - [ ] `login.html`
  - [ ] `signup.html`
  - [ ] `admin_dashboard.html`
  - [ ] `applicant_dashboard.html`
  - [ ] `employer_dashboard.html`
  - [ ] All other template files

### Static Files (entire folder)
- [ ] `static/` folder with:
  - [ ] `images/` subfolder
  - [ ] `uploads/` subfolder (if exists)
  - [ ] `screenings/` subfolder (if exists)
  - [ ] All CSS, JS, and image files

### Database & Migration Files (if needed)
- [ ] `init_db.py` - Database initialization script
- [ ] `setup_database.py` - Database setup script
- [ ] `migrations/` folder (if using Flask-Migrate)

### Helper Scripts (optional but recommended)
- [ ] `setup_production.py` - Production setup script (created for you)
- [ ] `start_production.sh` - Startup script (created for you)

### Configuration Files
- [ ] `env_example.txt` - Environment variables example (created for you)
- [ ] `.gitignore` - Git ignore file (created for you)

## ❌ Files NOT to Upload

- [ ] `__pycache__/` folders - Python cache (not needed)
- [ ] `*.pyc` files - Compiled Python files
- [ ] `*.db` files - SQLite databases (you'll use MySQL)
- [ ] `*.bat` files - Windows batch files (not needed on Linux server)
- [ ] `.env` file - Environment variables (create on server)
- [ ] `instance/` folder with local databases
- [ ] `flask` file (if it's a local executable)

## 📝 Files to Create on Server

After uploading, create these on the server:

1. **`.env` file** (copy from `env_example.txt` and fill in values)
2. **`logs/` directory** (for application logs)
3. **`venv/` directory** (Python virtual environment - created via SSH)

## 🔍 Pre-Upload Checklist

Before uploading, make sure:

- [ ] You've updated `app.py` line 30 with Hostinger database credentials
- [ ] You've changed `app.py` line 25 secret key
- [ ] You've set `app.py` line 1566 to `debug=False`
- [ ] All sensitive information is removed or will be updated on server
- [ ] You've tested the application locally one last time

## 📦 Upload Methods

### Method 1: File Manager (Easiest)
1. Use Hostinger hPanel File Manager
2. Upload files via web interface
3. Best for: Small projects, beginners

### Method 2: FTP Client
1. Use FileZilla, WinSCP, or similar
2. Connect using FTP credentials from hPanel
3. Best for: Large projects, multiple files

### Method 3: Git (Advanced)
1. Push to GitHub/GitLab
2. Clone on server via SSH
3. Best for: Version control, updates

## 🎯 Quick Upload Command (If Using Git)

```bash
# On your local machine
git add .
git commit -m "Prepare for deployment"
git push origin main

# On server (via SSH)
cd ~/public_html/smarthire
git pull origin main
```

## ⚠️ Important Notes

1. **File Permissions:** Some files may need specific permissions (set via SSH)
2. **Large Files:** If you have large files in `static/`, consider using CDN
3. **Database:** Don't upload local database files - create fresh on server
4. **Environment:** Create `.env` file on server, never commit it

## 📊 File Size Considerations

- **Total upload size:** Should be reasonable (< 100MB typically)
- **Large dependencies:** Will be installed via `pip install` on server
- **spaCy model:** Will be downloaded on server (not uploaded)

---

**Ready to deploy?** Follow the steps in `HOSTINGER_DEPLOYMENT.md`!

