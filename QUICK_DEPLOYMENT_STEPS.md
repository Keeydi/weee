# Quick Deployment Steps - Hostinger (Cheat Sheet)

## 🚀 Fast Track Deployment (For Experienced Users)

### 1. Upload Files
```bash
# Upload all files to: ~/public_html/smarthire/
```

### 2. Create MySQL Database
- hPanel → Databases → Create Database
- Note: username, password, database name

### 3. SSH Commands
```bash
cd ~/public_html/smarthire
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
python -m spacy download en_core_web_sm
```

### 4. Configure Database
Edit `app.py` line 30:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/DATABASE_NAME'
```

### 5. Disable Debug Mode
Edit `app.py` line 1566:
```python
app.run(debug=False)  # Change from True to False
```

### 6. Initialize Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     exit()
```

### 7. Test Gunicorn
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

### 8. Setup PM2 (Keep Running)
```bash
npm install -g pm2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app
pm2 save
pm2 startup
```

### 9. Set Permissions
```bash
chmod -R 755 static templates
chmod -R 777 uploads resumes  # If these folders exist
```

### 10. Test
Visit: `http://yourdomain.com`

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | `source venv/bin/activate` then `pip install -r requirements.txt` |
| Database error | Check credentials in app.py line 30 |
| Permission denied | `chmod -R 755` on folders |
| App not loading | Check `pm2 list` and `pm2 logs smarthire` |
| Port in use | Change port in `gunicorn_config.py` |

---

## 📝 Files to Modify Before Deployment

1. **app.py** (Line 30): Database connection string
2. **app.py** (Line 25): Secret key (change from "secret123")
3. **app.py** (Line 1566): `debug=False`
4. **app.py** (Lines 57-59): Email credentials (optional, can keep as is)

---

## 🔑 Hostinger Database Format

Your database connection will look like:
```
mysql+pymysql://u123456789_admin:password@localhost/u123456789_smarthire
```

Where:
- `u123456789_admin` = Your database username (from hPanel)
- `password` = Your database password
- `u123456789_smarthire` = Your database name

---

## ✅ Final Checklist

- [ ] Files uploaded
- [ ] Database created and credentials updated
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Debug mode disabled
- [ ] Gunicorn tested
- [ ] PM2 running
- [ ] Permissions set
- [ ] Application accessible via domain

