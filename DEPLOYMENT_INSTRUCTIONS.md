# 🚀 SmartHire - Hostinger Deployment Instructions

**Follow these steps to deploy your SmartHire application to Hostinger.**

---

## ⚠️ IMPORTANT: Before You Start

1. **You need VPS or Cloud Hosting** (Shared hosting won't work)
2. **SSH Access must be enabled** in your Hostinger account
3. **All files must be uploaded** to the server first

---

## 📤 STEP 1: Upload Files to Hostinger

### Option A: Using File Manager (Easiest)

1. Log into [hpanel.hostinger.com](https://hpanel.hostinger.com)
2. Go to **File Manager**
3. Navigate to `public_html`
4. Create folder: `smarthire`
5. Upload ALL files:
   - ✅ `app.py`
   - ✅ `wsgi.py`
   - ✅ `gunicorn_config.py`
   - ✅ `requirements.txt`
   - ✅ `templates/` (entire folder)
   - ✅ `static/` (entire folder)
   - ✅ All other Python files

### Option B: Using FTP

1. Get FTP credentials from hPanel → FTP Accounts
2. Use FileZilla or similar
3. Connect and upload all files to `public_html/smarthire`

---

## 🗄️ STEP 2: Create MySQL Database

1. In hPanel → **Databases** → **MySQL Databases**
2. Click **"Create New Database"**
3. Name: `smarthire`
4. **COPY THESE CREDENTIALS:**
   - Database Name: `uXXXXX_smarthire`
   - Username: `uXXXXX_admin`
   - Password: (the one you set)
   - Host: `localhost`

**⚠️ SAVE THESE - You'll need them in Step 3!**

---

## ⚙️ STEP 3: Update app.py Configuration

1. In File Manager, open `app.py`
2. Edit these lines:

### Line 30 - Database Connection:
```python
# REPLACE THIS:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smarthire'

# WITH THIS (use your actual credentials):
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uXXXXX_admin:YOUR_PASSWORD@localhost/uXXXXX_smarthire'
```

### Line 25 - Secret Key:
```python
# REPLACE THIS:
app.secret_key = "secret123"

# WITH THIS (generate a random key):
app.secret_key = "your-very-long-random-secret-key-change-this"
```

**Generate secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Line 1566 - Debug Mode:
```python
# REPLACE THIS:
app.run(debug=True)

# WITH THIS:
app.run(debug=False)
```

3. **Save the file**

---

## 🔧 STEP 4: Access SSH Terminal

1. In hPanel → **SSH Access** → **Open Terminal**
2. Or use SSH client (PuTTY, Terminal, etc.)

---

## 🚀 STEP 5: Run Deployment Commands

**Copy and paste ALL commands from `HOSTINGER_DEPLOY_COMMANDS.txt`**

Or run them one by one:

```bash
# Navigate to project
cd ~/public_html/smarthire

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Download spaCy model
python -m spacy download en_core_web_sm

# Create directories
mkdir -p logs static/uploads static/screenings uploads resumes

# Set permissions
chmod -R 755 static templates
chmod -R 777 uploads resumes static/uploads static/screenings

# Initialize database
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("Database initialized!")
EOF

# Setup PM2
npm install -g pm2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app
pm2 save
pm2 startup
```

**Follow the command that `pm2 startup` gives you!**

---

## ✅ STEP 6: Verify Deployment

1. Check PM2 status:
   ```bash
   pm2 list
   pm2 logs smarthire
   ```

2. Visit your domain:
   - `http://yourdomain.com` or
   - `http://yourdomain.com/smarthire`

---

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Database connection error"
- Check `app.py` line 30 has correct credentials
- Verify database exists in hPanel
- Check MySQL is running

### "Permission denied"
```bash
chmod -R 755 ~/public_html/smarthire
```

### "App not loading"
```bash
pm2 restart smarthire
pm2 logs smarthire
```

### "Port already in use"
- Change port in `gunicorn_config.py`
- Or kill the process using the port

---

## 📞 Need Help?

1. **Hostinger Support:** Live chat in hPanel
2. **Check Logs:** `pm2 logs smarthire`
3. **Full Guide:** See `HOSTINGER_DEPLOYMENT.md`

---

## ✅ Deployment Checklist

- [ ] Files uploaded to server
- [ ] MySQL database created
- [ ] Database credentials updated in `app.py`
- [ ] Secret key changed
- [ ] Debug mode disabled
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] PM2 running
- [ ] Application accessible

---

**Good luck with your deployment!** 🚀

