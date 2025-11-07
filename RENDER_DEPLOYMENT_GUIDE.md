# SmartHire - Render.com Deployment Guide (Easiest Option!)

This is a step-by-step guide to deploy SmartHire on Render.com - the easiest deployment platform.

---

## 🎯 Why Render?

- ✅ **100% Free tier** (no credit card needed)
- ✅ **Automatic deployments** from GitHub
- ✅ **Built-in PostgreSQL** database
- ✅ **No SSH required** - everything in browser
- ✅ **Auto SSL** certificates
- ✅ **10-minute setup**

---

## 📋 Prerequisites

1. ✅ Your code pushed to GitHub
2. ✅ GitHub account
3. ✅ Email account (for Render signup)

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code on GitHub

If you haven't already:

```bash
# In your project folder
git init
git add .
git commit -m "Initial commit - ready for Render"
git branch -M main
git remote add origin https://github.com/Keeeeeeeeydi/smarthire.git
git push -u origin main
```

**Make sure these files exist:**
- ✅ `app.py`
- ✅ `wsgi.py`
- ✅ `gunicorn_config.py`
- ✅ `requirements.txt`

---

### Step 2: Create Render Account

1. Go to **[render.com](https://render.com)**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended - easiest)
4. Authorize Render to access your GitHub

---

### Step 3: Create PostgreSQL Database

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name:** `smarthire-db` (or your choice)
   - **Database:** `smarthire`
   - **User:** `smarthire_user` (auto-generated)
   - **Region:** Choose closest to you
   - **Plan:** **Free** (for testing)
4. Click **"Create Database"**
5. **IMPORTANT:** Copy the **"Internal Database URL"** - you'll need it!

**Example URL format:**
```
postgresql://smarthire_user:password@dpg-xxxxx-a/smarthire
```

---

### Step 4: Update Your Code for PostgreSQL

Since Render uses PostgreSQL (not MySQL), update your code:

#### 4.1 Update `requirements.txt`

Add PostgreSQL driver:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Mail==0.9.1
PyPDF2==3.0.1
spacy==3.7.2
scikit-learn==1.3.2
psycopg2-binary==2.9.9  # ← ADD THIS for PostgreSQL
Werkzeug==3.0.1
SQLAlchemy==2.0.23
gunicorn==21.2.0  # ← ADD THIS for production
```

#### 4.2 Update `app.py` Database Connection

Find line 30 in `app.py` and replace:

**OLD:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smarthire'
```

**NEW:**
```python
import os

# Get database URL from environment variable (Render provides this)
database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/smarthire')

# Convert postgres:// to postgresql:// if needed (for SQLAlchemy)
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
```

#### 4.3 Update `gunicorn_config.py`

Change the bind address:
```python
bind = "0.0.0.0:10000"  # Render uses port 10000
```

Or use environment variable:
```python
import os
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
```

#### 4.4 Commit Changes

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

---

### Step 5: Create Web Service on Render

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Select your `smarthire` repository
4. Configure the service:

   **Basic Settings:**
   - **Name:** `smarthire` (or your choice)
   - **Region:** Same as your database
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or `./` if code is in subfolder)
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command:**
     ```bash
     gunicorn -c gunicorn_config.py wsgi:app
     ```

5. Click **"Advanced"** → **"Add Environment Variable"**

   Add these variables:
   ```
   PYTHON_VERSION=3.11.0
   FLASK_ENV=production
   SECRET_KEY=your-very-long-random-secret-key-here-change-this
   DATABASE_URL=postgresql://... (paste from Step 3)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-gmail-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

6. Click **"Create Web Service"**

---

### Step 6: Wait for Deployment

Render will:
1. ✅ Clone your repository
2. ✅ Install dependencies
3. ✅ Download spaCy model
4. ✅ Start your application

**This takes 5-10 minutes** ⏱️

You'll see build logs in real-time. Watch for any errors!

---

### Step 7: Initialize Database

Once deployment is complete:

1. Go to your web service URL (e.g., `https://smarthire.onrender.com`)
2. You might see an error - that's normal if database isn't initialized
3. Open Render **Shell** (in your web service):
   - Click on your web service
   - Go to **"Shell"** tab
   - Click **"Open Shell"**

4. Run database initialization:
   ```bash
   python
   ```
   Then in Python:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
       print("Database tables created!")
       exit()
   ```

5. Or use your setup script:
   ```bash
   python init_db.py
   ```

---

### Step 8: Test Your Application

1. Visit your Render URL: `https://smarthire.onrender.com`
2. Test signup/login
3. Test file uploads
4. Check database in Render dashboard

**✅ Your app is live!**

---

## 🔧 Configuration Details

### Environment Variables Explained

| Variable | Value | Notes |
|----------|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version to use |
| `FLASK_ENV` | `production` | Production mode |
| `SECRET_KEY` | Random string | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Auto from Render | PostgreSQL connection string |
| `MAIL_*` | Your email settings | Gmail App Password |

### Generate Secret Key

In your local terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and use it as `SECRET_KEY`

---

## 📁 File Structure for Render

Your project should have:
```
smarthire/
├── app.py
├── wsgi.py
├── gunicorn_config.py
├── requirements.txt
├── templates/
├── static/
└── (other files)
```

---

## 🔄 Automatic Deployments

**Render automatically deploys when you push to GitHub!**

1. Make changes locally
2. Commit: `git commit -m "Update feature"`
3. Push: `git push origin main`
4. Render detects changes
5. Automatically rebuilds and redeploys

**No manual deployment needed!** 🎉

---

## 🗄️ Database Management

### Access Database

1. Go to your PostgreSQL service in Render
2. Click **"Connect"** → **"External Connection"**
3. Use connection string with database tools like:
   - **pgAdmin**
   - **DBeaver**
   - **TablePlus**

### View Data

Use Render's **"Shell"** to access database:
```bash
psql $DATABASE_URL
```

Then SQL commands:
```sql
\dt  -- List tables
SELECT * FROM "User";  -- View users
```

---

## 🐛 Troubleshooting

### Issue: Build Fails

**Check:**
- ✅ All dependencies in `requirements.txt`
- ✅ Python version compatibility
- ✅ Build command is correct

**Solution:**
- Check build logs in Render
- Fix errors and push again

### Issue: App Crashes on Start

**Check:**
- ✅ `gunicorn_config.py` bind address
- ✅ Environment variables are set
- ✅ Database URL is correct

**Solution:**
- Check logs in Render dashboard
- Verify all environment variables

### Issue: Database Connection Error

**Check:**
- ✅ `DATABASE_URL` is set correctly
- ✅ Database is running (check in Render)
- ✅ Connection string format is correct

**Solution:**
- Re-copy `DATABASE_URL` from database service
- Make sure it starts with `postgresql://`

### Issue: File Uploads Not Working

**Note:** Render's file system is **ephemeral** (files disappear on restart)

**Solution:** Use cloud storage:
- AWS S3
- Cloudinary
- Or store file paths in database

---

## 💰 Pricing

### Free Tier Includes:
- ✅ 750 hours/month (enough for 1 app running 24/7)
- ✅ 512 MB RAM
- ✅ PostgreSQL database (90 days retention)
- ✅ SSL certificates
- ✅ Automatic deployments

### Paid Plans:
- **Starter:** $7/month (more resources)
- **Standard:** $25/month (production-ready)

**Free tier is perfect for testing and small projects!**

---

## 🔒 Security Notes

1. **Never commit `.env` files** to GitHub
2. **Use strong `SECRET_KEY`** (generate randomly)
3. **Keep `DATABASE_URL` secret** (Render handles this)
4. **Use Gmail App Password** (not regular password)
5. **Enable 2FA** on your GitHub account

---

## 📊 Monitoring

### View Logs

1. Go to your web service in Render
2. Click **"Logs"** tab
3. See real-time application logs

### Metrics

Render shows:
- ✅ CPU usage
- ✅ Memory usage
- ✅ Request count
- ✅ Response times

---

## 🎯 Next Steps

1. ✅ **Test your application** thoroughly
2. ✅ **Set up custom domain** (optional):
   - Go to web service → Settings
   - Add custom domain
   - Update DNS records
3. ✅ **Set up monitoring** (optional)
4. ✅ **Backup database** regularly

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Code updated for PostgreSQL
- [ ] Web service created
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Database initialized
- [ ] Application tested
- [ ] Logs checked

---

## 🆘 Need Help?

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **Render Support:** [render.com/support](https://render.com/support)
- **Community:** [community.render.com](https://community.render.com)

---

## 🎉 Congratulations!

Your SmartHire application is now live on Render! 🚀

**Your URL:** `https://smarthire.onrender.com` (or your custom domain)

---

**Last Updated:** Render deployment guide for SmartHire

