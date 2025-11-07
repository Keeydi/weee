# 🚀 Deploy New SmartHire - Step by Step

Follow these steps in your Hostinger SSH terminal:

---

## STEP 1: Navigate to Project Directory

```bash
cd /var/www/smarthire
pwd
```

---

## STEP 2: Clone from GitHub (if code is on GitHub)

```bash
git clone https://github.com/Keeeeeeeeydi/smarthire.git .
```

**OR** if you need to upload files manually, skip to Step 3.

---

## STEP 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## STEP 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

## STEP 5: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

If that fails:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

---

## STEP 6: Create Directories

```bash
mkdir -p logs
mkdir -p static/uploads
mkdir -p static/screenings
mkdir -p uploads
mkdir -p resumes
mkdir -p screened_resumes
```

---

## STEP 7: Set Permissions

```bash
chmod -R 755 static templates
chmod -R 777 uploads resumes static/uploads static/screenings
```

---

## STEP 8: Update app.py Configuration

**IMPORTANT:** You need to edit `app.py` with your database credentials.

1. Create MySQL database in hPanel first
2. Then update `app.py` line 30 with your database connection string
3. Update line 25 with a new secret key
4. Update line 1566 to set `debug=False`

---

## STEP 9: Initialize Database

```bash
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Database initialized!")
EOF
```

---

## STEP 10: Test Gunicorn

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

Press `Ctrl+C` after testing.

---

## STEP 11: Setup PM2 (Keep Running)

```bash
npm install -g pm2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app
pm2 save
pm2 startup
```

Follow the command that `pm2 startup` gives you!

---

## STEP 12: Check Status

```bash
pm2 list
pm2 logs smarthire
```

---

## ✅ DONE!

Your app should be live!


