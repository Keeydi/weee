# Hostinger Deployment - Quick Reference

Quick guide for deploying SmartHire on Hostinger VPS/Cloud hosting.

---

## 🎯 Hostinger Overview

### What You Need:
- ✅ **VPS or Cloud Hosting** (Shared hosting won't work for Flask)
- ✅ **SSH Access** enabled
- ✅ **Domain name** connected
- ✅ **Python 3.8+** on server

### Why Hostinger?
- ✅ Full control over server
- ✅ Can use MySQL (your current setup)
- ✅ Persistent file storage
- ✅ No cold starts
- ⚠️ Requires more technical knowledge

---

## ⚡ Quick Deployment Steps

### 1. Upload Files
- Use **File Manager** in hPanel OR **FTP**
- Upload to: `~/public_html/smarthire/`

### 2. Create MySQL Database
- hPanel → **Databases** → **MySQL Databases**
- Create database: `smarthire`
- Note: username, password, database name (with `u123456789_` prefix)

### 3. Update Database Connection
Edit `app.py` line 30:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/DATABASE_NAME'
```

Example:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u123456789_admin:mypassword@localhost/u123456789_smarthire'
```

### 4. Access SSH/Terminal
- hPanel → **SSH Access** → **Open Terminal**

### 5. Setup Python Environment
```bash
cd ~/public_html/smarthire
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
python -m spacy download en_core_web_sm
```

### 6. Update Production Settings
Edit `app.py`:
- Line 25: Change secret key from "secret123"
- Line 1566: Change `debug=False`

### 7. Initialize Database
```bash
python
```
Then:
```python
from app import app, db
with app.app_context():
    db.create_all()
    exit()
```

### 8. Test Gunicorn
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

### 9. Setup PM2 (Keep Running)
```bash
npm install -g pm2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app
pm2 save
pm2 startup
```

### 10. Set Permissions
```bash
chmod -R 755 static templates
chmod -R 777 uploads resumes  # If these folders exist
```

---

## 📋 Configuration Checklist

- [ ] Files uploaded to server
- [ ] MySQL database created
- [ ] Database credentials updated in `app.py` line 30
- [ ] Secret key changed (line 25)
- [ ] Debug mode disabled (line 1566)
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] spaCy model downloaded
- [ ] Database initialized
- [ ] Gunicorn tested
- [ ] PM2 running
- [ ] File permissions set
- [ ] Application accessible

---

## 🔧 Key Files to Update

### `app.py` Changes:

**Line 30 - Database:**
```python
# OLD:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smarthire'

# NEW (Hostinger format):
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u123456789_admin:password@localhost/u123456789_smarthire'
```

**Line 25 - Secret Key:**
```python
# OLD:
app.secret_key = "secret123"

# NEW:
app.secret_key = "your-very-long-random-secret-key-here"
```

**Line 1566 - Debug Mode:**
```python
# OLD:
app.run(debug=True)

# NEW:
app.run(debug=False)
```

---

## 🗄️ Hostinger Database Format

Hostinger adds a prefix to database names and usernames:

**Format:**
```
u[account_number]_[your_name]
```

**Example:**
- Database Name: `u123456789_smarthire`
- Username: `u123456789_admin`
- Password: (the one you set)
- Host: `localhost`

**Connection String:**
```
mysql+pymysql://u123456789_admin:password@localhost/u123456789_smarthire
```

---

## 🐛 Common Issues

### Issue: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Database connection error"
- Check credentials in `app.py` line 30
- Verify database exists in hPanel
- Check MySQL service is running

### Issue: "Permission denied"
```bash
chmod -R 755 ~/public_html/smarthire
chmod -R 777 ~/public_html/smarthire/uploads
```

### Issue: "App not loading"
```bash
pm2 list          # Check if running
pm2 logs smarthire  # Check logs
```

### Issue: "Port already in use"
- Change port in `gunicorn_config.py`
- Or kill process using the port

---

## 📞 Getting Help

1. **Hostinger Support:** Live chat in hPanel (24/7)
2. **Check Logs:** 
   - `pm2 logs smarthire`
   - hPanel → Logs
3. **Full Guide:** See `HOSTINGER_DEPLOYMENT.md`

---

## 🆚 Hostinger vs Other Platforms

| Feature | Hostinger | Render | Railway |
|---------|-----------|--------|---------|
| **Difficulty** | ⭐⭐⭐⭐ Hard | ⭐ Easy | ⭐ Easy |
| **Setup Time** | 1-2 hours | 10 min | 10 min |
| **File Storage** | ✅ Persistent | ⚠️ Ephemeral | ⚠️ Ephemeral |
| **Database** | ✅ MySQL | ✅ PostgreSQL | ✅ PostgreSQL |
| **SSH Access** | ✅ Yes | ❌ No | ❌ No |
| **Full Control** | ✅ Yes | ❌ No | ❌ No |
| **Best For** | Advanced users | Beginners | Beginners |

---

## 💡 Recommendation

**If you're a beginner:**
- 👉 Use **Render** or **Railway** (much easier)

**If you need:**
- Full server control
- MySQL (not PostgreSQL)
- Persistent file storage
- Custom configurations
- 👉 Use **Hostinger**

---

## 📚 Full Documentation

For complete step-by-step instructions, see:
- **`HOSTINGER_DEPLOYMENT.md`** - Complete 16-step guide
- **`QUICK_DEPLOYMENT_STEPS.md`** - Fast reference

---

**Need help?** Check the full guide or contact Hostinger support! 🚀

