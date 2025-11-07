# SmartHire - Hostinger Deployment Guide (Step-by-Step for Beginners)

This guide will walk you through deploying your SmartHire Flask application to Hostinger hosting.

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ A Hostinger account (VPS or Cloud hosting recommended)
- ✅ Your domain name connected to Hostinger
- ✅ Access to Hostinger hPanel (control panel)
- ✅ Your application files ready

---

## 🎯 Step 1: Choose Your Hosting Plan

**Important:** Flask applications require **VPS or Cloud hosting** on Hostinger. Shared hosting typically doesn't support Flask applications well.

### Recommended Plans:
- **VPS Hosting** (minimum 1GB RAM)
- **Cloud Hosting** (Business or higher)

If you only have shared hosting, you may need to upgrade. Contact Hostinger support if unsure.

---

## 🔧 Step 2: Access Your Hostinger hPanel

1. Log in to your Hostinger account at [hpanel.hostinger.com](https://hpanel.hostinger.com)
2. Go to **hPanel** (Hostinger's control panel)
3. Find your domain/hosting plan
4. Look for **"SSH Access"** or **"Terminal"** option
   - If SSH is not enabled, you may need to enable it in hPanel
   - Some plans require you to request SSH access from support

---

## 📤 Step 3: Upload Your Files

### Option A: Using File Manager (Easiest for Beginners)

1. In hPanel, click **"File Manager"**
2. Navigate to your domain's root directory (usually `public_html` or `domains/yourdomain.com/public_html`)
3. Create a new folder called `smarthire` (or your preferred name)
4. Upload all your project files:
   - `app.py`
   - `requirements.txt`
   - All files from `templates/` folder
   - All files from `static/` folder
   - `db_connector.py`
   - Any other Python files

**Note:** Do NOT upload:
- `__pycache__/` folders
- `.db` files (SQLite databases - you'll use MySQL instead)
- `*.bat` files (Windows batch files - not needed on server)

### Option B: Using FTP (Alternative)

1. In hPanel, find **"FTP Accounts"**
2. Create an FTP account if you don't have one
3. Use an FTP client (like FileZilla) to upload files
4. Connect using the FTP credentials provided

---

## 🗄️ Step 4: Set Up MySQL Database

1. In hPanel, go to **"Databases"** → **"MySQL Databases"**
2. Click **"Create New Database"**
3. Name it: `smarthire` (or your preferred name)
4. Note down:
   - **Database Name**: `u123456789_smarthire` (Hostinger format)
   - **Database Username**: `u123456789_admin` (Hostinger format)
   - **Database Password**: (the one you set)
   - **Database Host**: Usually `localhost` (check in hPanel)

5. Click **"Create"**

**Important:** Save these credentials - you'll need them in the next step!

---

## ⚙️ Step 5: Configure Your Application

### 5.1 Update Database Connection

You need to update `app.py` with your Hostinger MySQL credentials. 

**Find line 30 in app.py** and replace it with:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/DATABASE_NAME'
```

**Hostinger Database Format Example:**
```
mysql+pymysql://u123456789_admin:yourpassword@localhost/u123456789_smarthire
```

**Where to find these values:**
- In hPanel → Databases → MySQL Databases
- You'll see: Database Name, Username, Password
- Host is usually `localhost` (check in hPanel if different)

**Important:** Hostinger adds a prefix like `u123456789_` to database names and usernames. Make sure to include the full name!

### 5.2 Update Production Settings in app.py

**IMPORTANT:** You need to modify `app.py` for production:

1. **Change Secret Key (Line 25):**
   ```python
   app.secret_key = "your-very-long-random-secret-key-here"  # Change from "secret123"
   ```
   Generate a random key: You can use Python: `import secrets; print(secrets.token_hex(32))`

2. **Disable Debug Mode (Line 1566):**
   ```python
   app.run(debug=False)  # Change from True to False
   ```

3. **Update Email Settings (Lines 57-59):** 
   - Keep your current email settings or update if needed
   - Make sure Gmail App Password is correct

**Note:** For now, we'll keep the database connection directly in app.py. Advanced users can use environment variables later.

---

## 🐍 Step 6: Set Up Python Environment

### 6.1 Access SSH/Terminal

**Option A: Using hPanel Terminal (Easiest)**
1. In hPanel, find **"SSH Access"** or **"Terminal"**
2. Click **"Open Terminal"** or **"Launch Terminal"**
3. You'll see a web-based terminal

**Option B: Using SSH Client (Advanced)**
1. In hPanel → SSH Access, note your SSH details:
   - Host: Usually `ssh.yourdomain.com` or IP address
   - Port: Usually `22`
   - Username: Your Hostinger username (usually starts with `u`)
   - Password: Your Hostinger password
2. Use an SSH client like:
   - **Windows:** PuTTY, Windows Terminal, or Git Bash
   - **Mac/Linux:** Built-in Terminal
3. Connect: `ssh username@host -p 22`

### 6.2 Navigate to Your Project

**Find your project path:**
- Usually: `~/public_html/smarthire`
- Or: `~/domains/yourdomain.com/public_html/smarthire`
- Check in File Manager to confirm the exact path

```bash
# Try this first:
cd ~/public_html/smarthire

# If that doesn't work, try:
cd ~/domains/yourdomain.com/public_html/smarthire

# List files to confirm you're in the right place:
ls -la
```

### 6.3 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Unix
```

### 6.4 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

### 6.5 Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

**Note:** This may take a few minutes. If it fails, try:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

---

## 🔐 Step 7: Configure Production Settings

### 7.1 Update app.py for Production

**You should have already done this in Step 5, but double-check:**

1. **Line 30:** Database connection string updated with Hostinger MySQL credentials
2. **Line 25:** Secret key changed from "secret123" to a strong random key
3. **Line 1566:** `debug=False` (not `True`)

**Quick verification:**
```bash
# Check if debug is disabled
grep "debug=" app.py
# Should show: app.run(debug=False)
```

---

## 🚀 Step 8: Create WSGI Entry Point

Create a file called `wsgi.py` in your project root:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

---

## 🔄 Step 9: Initialize Database

**Option A: Using Python Interactive Shell**

In the SSH terminal:

```bash
cd ~/public_html/smarthire
source venv/bin/activate
python3
```

Then in Python (type these commands one by one):
```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    exit()
```

**Option B: Using Your Setup Script**

If you uploaded `init_db.py`:
```bash
cd ~/public_html/smarthire
source venv/bin/activate
python3 init_db.py
```

**Option C: Using Production Setup Script**

If you uploaded `setup_production.py`:
```bash
cd ~/public_html/smarthire
source venv/bin/activate
python3 setup_production.py
```

**Verify:** Check in hPanel → phpMyAdmin that tables were created.

---

## 🌐 Step 10: Configure Web Server

### Option A: Using Gunicorn (Recommended)

**The `gunicorn_config.py` file should already be in your project.** If not, create it (see the file I created for you).

**Test Gunicorn:**
```bash
cd ~/public_html/smarthire
source venv/bin/activate

# Create logs directory first
mkdir -p logs

# Test Gunicorn (this will start the server)
gunicorn -c gunicorn_config.py wsgi:app
```

**If it works, you'll see:**
```
[INFO] Starting gunicorn 20.x.x
[INFO] Listening at: http://127.0.0.1:8000
[INFO] Using worker: sync
[INFO] Booting worker with pid: xxxxx
```

**Press Ctrl+C to stop it.** We'll set up PM2 next to keep it running.

### Option B: Using Passenger (If Available)

If Hostinger supports Passenger, create `passenger_wsgi.py`:
```python
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from app import app as application
```

---

## 📝 Step 11: Create Startup Script

Create a file `start.sh`:

```bash
#!/bin/bash
cd /home/u123456789/domains/yourdomain.com/public_html/smarthire
source venv/bin/activate
gunicorn -c gunicorn_config.py wsgi:app
```

Make it executable:
```bash
chmod +x start.sh
```

---

## 🔄 Step 12: Set Up Process Manager (PM2 or Supervisor)

### Using PM2 (Recommended):

**First, check if Node.js/npm is available:**
```bash
node --version
npm --version
```

**If Node.js is not installed, you may need to:**
1. Install it via hPanel (if available)
2. Or use Supervisor instead (see below)
3. Or contact Hostinger support to install Node.js

**If Node.js is available:**
```bash
# Install PM2 globally
npm install -g pm2

# Navigate to project
cd ~/public_html/smarthire

# Start application with PM2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app

# Save PM2 configuration
pm2 save

# Setup PM2 to start on server reboot
pm2 startup
# Follow the instructions it gives you (usually run a command it provides)

# Check status
pm2 list
pm2 logs smarthire
```

**PM2 Commands:**
- `pm2 list` - See all running apps
- `pm2 logs smarthire` - View logs
- `pm2 restart smarthire` - Restart app
- `pm2 stop smarthire` - Stop app
- `pm2 delete smarthire` - Remove from PM2

### Using Supervisor (Alternative - If PM2 not available):

**Note:** Supervisor usually requires root access. You may need to contact Hostinger support.

1. Create configuration file (you may need to ask Hostinger support where to place it):
```ini
[program:smarthire]
command=/home/u123456789/public_html/smarthire/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
directory=/home/u123456789/public_html/smarthire
user=u123456789
autostart=true
autorestart=true
stdout_logfile=/home/u123456789/public_html/smarthire/logs/supervisor.log
stderr_logfile=/home/u123456789/public_html/smarthire/logs/supervisor_error.log
```

2. Update Supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smarthire
```

**Alternative: Simple Background Process (Temporary Solution)**

If PM2 and Supervisor aren't available, you can run in background:
```bash
cd ~/public_html/smarthire
source venv/bin/activate
nohup gunicorn -c gunicorn_config.py wsgi:app > logs/app.log 2>&1 &
```

**Note:** This is not ideal for production but works as a temporary solution.

---

## 📁 Step 13: Set File Permissions

```bash
chmod 755 ~/public_html/smarthire
chmod -R 755 ~/public_html/smarthire/static
chmod -R 755 ~/public_html/smarthire/templates
chmod -R 777 ~/public_html/smarthire/uploads  # If you have uploads folder
chmod -R 777 ~/public_html/smarthire/resumes  # If you have resumes folder
```

---

## 🔗 Step 14: Configure Domain/Subdomain

**Option A: Use Main Domain (Recommended for beginners)**

1. Your main domain should already point to `public_html`
2. If your app is in `public_html/smarthire`, you can:
   - Move all files to `public_html` (root), OR
   - Create a redirect/index.html in root that redirects to `/smarthire`

**Option B: Create Subdomain**

1. In hPanel, go to **"Domains"** → **"Subdomains"**
2. Create a new subdomain (e.g., `app.yourdomain.com`)
3. Point it to: `public_html/smarthire`
4. Wait a few minutes for DNS to propagate

**Option C: Use Subdirectory**

1. Access your app at: `http://yourdomain.com/smarthire`
2. No additional configuration needed

**For Production, Option A (root domain) is usually best.**

---

## 🧪 Step 15: Configure Reverse Proxy (If Needed)

**If your app doesn't load directly, you may need to configure a reverse proxy.**

Hostinger VPS/Cloud hosting usually uses Nginx. You may need to:

1. **Contact Hostinger Support** to configure Nginx reverse proxy, OR
2. **If you have access to Nginx config**, add this to your site configuration:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Note:** Most beginners should contact Hostinger support for this step.

---

## 🧪 Step 16: Test Your Application

1. Visit your domain: `http://yourdomain.com` or `http://app.yourdomain.com`
2. Check if the application loads
3. Test login functionality
4. Check database connectivity
5. Test file uploads (if applicable)

**If you see errors:**
- Check PM2 logs: `pm2 logs smarthire`
- Check Gunicorn logs: `cat logs/error.log`
- Check Hostinger error logs in hPanel

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and all dependencies are installed

### Issue: "Database connection error"
**Solution:** 
- Verify MySQL credentials in hPanel
- Check database name format (Hostinger uses `u123456789_` prefix)
- Ensure MySQL service is running

### Issue: "Permission denied"
**Solution:** Check file permissions with `ls -la` and fix with `chmod`

### Issue: "Port already in use"
**Solution:** Change the port in `gunicorn_config.py`

### Issue: "Application not loading"
**Solution:** 
- Check Gunicorn/PM2 is running: `pm2 list` or `ps aux | grep gunicorn`
- Check error logs: `pm2 logs smarthire`
- Check Hostinger error logs in hPanel

---

## 📞 Getting Help

1. **Hostinger Support:** Contact via live chat in hPanel
2. **Check Logs:** 
   - Application logs: `pm2 logs smarthire`
   - Server logs: Check in hPanel → Logs
3. **Common Issues:** See troubleshooting section above

---

## ✅ Deployment Checklist

- [ ] Files uploaded to server
- [ ] MySQL database created
- [ ] Database credentials updated in app.py
- [ ] Python virtual environment created
- [ ] Dependencies installed
- [ ] spaCy model installed
- [ ] Database initialized
- [ ] Gunicorn configured
- [ ] Process manager (PM2) set up
- [ ] File permissions set correctly
- [ ] Domain/subdomain configured
- [ ] Application tested and working
- [ ] Email configuration updated (if needed)
- [ ] Debug mode disabled

---

## 🔒 Security Reminders

1. **Never commit `.env` file** to version control
2. **Change default secret key** in production
3. **Use strong database passwords**
4. **Keep dependencies updated**
5. **Disable debug mode** in production
6. **Use HTTPS** (SSL certificate - usually free in Hostinger)

---

## 📚 Additional Resources

- [Hostinger Knowledge Base](https://www.hostinger.com/tutorials)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

**Good luck with your deployment! 🚀**

