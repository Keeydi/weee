# 🚀 Deploy SmartHire to Hostinger - RIGHT NOW!

This guide will help you deploy immediately.

---

## ⚡ Quick Deployment Steps

### Step 1: Log into Hostinger

1. Go to [hpanel.hostinger.com](https://hpanel.hostinger.com)
2. Login with your credentials
3. Open **File Manager**

---

### Step 2: Upload Files

1. In File Manager, go to `public_html`
2. Create folder: `smarthire`
3. Upload ALL files from your project:
   - `app.py`
   - `wsgi.py`
   - `gunicorn_config.py`
   - `requirements.txt`
   - `templates/` folder (entire folder)
   - `static/` folder (entire folder)
   - All other Python files

**Quick Upload:**
- Select all files in your local `SmartHire` folder
- Upload via File Manager or use FTP

---

### Step 3: Create MySQL Database

1. In hPanel → **Databases** → **MySQL Databases**
2. Click **"Create New Database"**
3. Name: `smarthire`
4. **IMPORTANT:** Copy these credentials:
   - Database Name: `uXXXXX_smarthire`
   - Username: `uXXXXX_admin`
   - Password: (the one you set)
   - Host: `localhost`

---

### Step 4: Update Database Connection

1. In File Manager, open `app.py`
2. Find line 30
3. Replace with:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/DATABASE_NAME'
   ```
   Replace USERNAME, PASSWORD, DATABASE_NAME with your actual values

4. Find line 25, change secret key:
   ```python
   app.secret_key = "change-this-to-random-key"
   ```

5. Find line 1566, change to:
   ```python
   app.run(debug=False)
   ```

---

### Step 5: Access SSH Terminal

1. In hPanel → **SSH Access** → **Open Terminal**
2. Navigate to project:
   ```bash
   cd ~/public_html/smarthire
   ```

---

### Step 6: Run Deployment Script

Copy and paste this entire block:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
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
```

---

### Step 7: Test Gunicorn

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

If it works, press `Ctrl+C` to stop.

---

### Step 8: Setup PM2 (Keep Running)

```bash
npm install -g pm2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app
pm2 save
pm2 startup
```

Follow the instructions `pm2 startup` gives you.

---

### Step 9: Check Status

```bash
pm2 list
pm2 logs smarthire
```

---

### Step 10: Access Your App!

Visit: `http://yourdomain.com` or `http://yourdomain.com/smarthire`

---

## ✅ Done!

Your app should now be live!

---

## 🆘 Troubleshooting

**Issue: Module not found**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Issue: Database error**
- Check credentials in `app.py` line 30
- Verify database exists in hPanel

**Issue: Permission denied**
```bash
chmod -R 755 ~/public_html/smarthire
```

**Issue: App not loading**
```bash
pm2 restart smarthire
pm2 logs smarthire
```

---

**Ready? Start with Step 1!** 🚀

