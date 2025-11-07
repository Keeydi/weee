# SmartHire - Vercel Deployment Guide

This guide covers deploying your Flask application on Vercel. Note: Vercel is optimized for serverless functions, so Flask apps require some adaptation.

---

## 🎯 Why Vercel?

- ✅ **Free tier** available
- ✅ **Automatic deployments** from GitHub
- ✅ **Global CDN** (fast worldwide)
- ✅ **Auto SSL** certificates
- ✅ **Serverless** architecture
- ⚠️ **Requires adaptation** for Flask apps

---

## ⚠️ Important Considerations

### Vercel Limitations for Flask:

1. **Serverless Functions:** Flask routes become serverless functions
2. **No Persistent File Storage:** Uploads need cloud storage (S3, Cloudinary)
3. **Cold Starts:** First request may be slower
4. **Database:** Use external database (PostgreSQL, MongoDB, etc.)
5. **Session Storage:** Use external session storage (Redis, database)

### Best For:
- ✅ Small to medium Flask apps
- ✅ Apps with external database
- ✅ Apps using cloud storage for files
- ✅ Apps that can be adapted to serverless

---

## 📋 Prerequisites

1. ✅ Code pushed to GitHub
2. ✅ Vercel account (free)
3. ✅ External database (PostgreSQL recommended)
4. ✅ Cloud storage for file uploads (optional but recommended)

---

## 🚀 Step-by-Step Deployment

### Step 1: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

Or use the web interface (no CLI needed).

---

### Step 2: Create `vercel.json` Configuration

Create a `vercel.json` file in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

---

### Step 3: Create `api/index.py` (Serverless Entry Point)

Create an `api` folder and `api/index.py` file:

```python
# api/index.py
from app import app

# Vercel serverless function handler
def handler(request):
    return app(request.environ, request.start_response)
```

**OR** use the simpler approach - create `vercel_app.py`:

```python
# vercel_app.py
from app import app

# Export the Flask app for Vercel
handler = app
```

---

### Step 4: Update `vercel.json` for Flask

Update `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "vercel_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "vercel_app.py"
    }
  ]
}
```

---

### Step 5: Update `app.py` for Vercel

Add this at the end of `app.py` (after the `if __name__ == "__main__"` block):

```python
# For Vercel serverless
if __name__ != "__main__":
    # Vercel will use this
    handler = app
```

**OR** create `vercel_app.py` (recommended):

```python
# vercel_app.py
from app import app

# Vercel serverless handler
handler = app
```

---

### Step 6: Update Database Connection

Vercel requires environment variables. Update `app.py` database connection:

```python
import os

# Get database URL from environment variable
database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/smarthire')

# Convert postgres:// to postgresql:// if needed
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
```

---

### Step 7: Handle File Uploads (Important!)

Vercel's file system is **read-only**. You **cannot** save files locally.

**Options:**

1. **Use Cloud Storage** (Recommended):
   - AWS S3
   - Cloudinary
   - Google Cloud Storage

2. **Store in Database:**
   - Convert PDFs to base64
   - Store in database (not recommended for large files)

3. **Use External Service:**
   - Upload directly to cloud storage from frontend

**Example with Cloudinary:**

```python
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# In upload route:
result = cloudinary.uploader.upload(file, resource_type="raw")
file_url = result['secure_url']
```

---

### Step 8: Update `requirements.txt`

Make sure you have:

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Mail==0.9.1
PyPDF2==3.0.1
spacy==3.7.2
scikit-learn==1.3.2
psycopg2-binary==2.9.9  # For PostgreSQL
Werkzeug==3.0.1
SQLAlchemy==2.0.23
```

---

### Step 9: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Easiest)

1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click **"New Project"**
4. Import your GitHub repository: `Keeeeeeeeydi/smarthire`
5. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `./` (or leave empty)
   - **Build Command:** Leave empty (Vercel auto-detects)
   - **Output Directory:** Leave empty
6. Add Environment Variables:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-secret-key
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```
7. Click **"Deploy"**

#### Option B: Using Vercel CLI

```bash
# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? smarthire
# - Directory? ./
# - Override settings? No
```

---

### Step 10: Set Up Database

Vercel doesn't provide databases. You need an external database:

**Options:**
1. **Render PostgreSQL** (free tier)
2. **Railway PostgreSQL** (free tier)
3. **Supabase** (free tier)
4. **Neon** (free tier)
5. **PlanetScale** (MySQL, free tier)

**Recommended:** Use Render PostgreSQL (see `RENDER_DEPLOYMENT_GUIDE.md` for database setup)

---

### Step 11: Configure Environment Variables

In Vercel dashboard → Your Project → Settings → Environment Variables:

Add:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
PYTHON_VERSION=3.11
```

---

### Step 12: Initialize Database

After deployment:

1. Go to your Vercel project
2. Open **"Functions"** tab
3. Use Vercel CLI or connect via external tool to initialize database

**Or use Vercel CLI:**

```bash
vercel env pull .env.local
python
```

Then:
```python
from app import app, db
with app.app_context():
    db.create_all()
    exit()
```

---

## 🔧 Vercel-Specific Configuration

### Handle Static Files

Vercel serves static files automatically from `static/` folder. Make sure your Flask app uses:

```python
app = Flask(__name__, static_folder='static', static_url_path='/static')
```

### Handle Sessions

Vercel serverless functions are stateless. Use:

1. **Database sessions:**
   ```python
   from flask_session import Session
   app.config['SESSION_TYPE'] = 'sqlalchemy'
   Session(app)
   ```

2. **Or use JWT tokens** instead of sessions

### Handle File Uploads

**Must use cloud storage!** Local file system is read-only.

---

## 📁 Project Structure for Vercel

```
smarthire/
├── api/
│   └── index.py          # Serverless entry point (optional)
├── vercel_app.py         # Vercel handler (recommended)
├── vercel.json           # Vercel configuration
├── app.py                # Main Flask app
├── requirements.txt
├── static/               # Served automatically
├── templates/            # Served automatically
└── .vercelignore         # Files to ignore (optional)
```

---

## 🐛 Troubleshooting

### Issue: "Function not found"

**Solution:**
- Make sure `vercel.json` points to correct file
- Check that `vercel_app.py` or `api/index.py` exists
- Verify handler is exported correctly

### Issue: "Database connection error"

**Solution:**
- Check `DATABASE_URL` environment variable
- Verify database is accessible from internet
- Check database firewall settings

### Issue: "File upload fails"

**Solution:**
- Vercel file system is read-only
- **Must use cloud storage** (S3, Cloudinary, etc.)
- Cannot save files locally on Vercel

### Issue: "Session not working"

**Solution:**
- Use database sessions or JWT tokens
- Serverless functions are stateless
- Cannot use file-based sessions

### Issue: "Cold start slow"

**Solution:**
- First request after inactivity is slower
- This is normal for serverless
- Consider keeping function warm with cron job

---

## 💰 Pricing

### Free Tier Includes:
- ✅ 100GB bandwidth/month
- ✅ Unlimited serverless function executions
- ✅ Automatic SSL
- ✅ Global CDN
- ✅ Automatic deployments

### Paid Plans:
- **Pro:** $20/month (more features)
- **Enterprise:** Custom pricing

**Free tier is great for testing and small projects!**

---

## ⚠️ Limitations & Workarounds

| Limitation | Workaround |
|------------|------------|
| No local file storage | Use cloud storage (S3, Cloudinary) |
| Stateless functions | Use database sessions or JWT |
| Cold starts | Acceptable for most apps |
| No persistent processes | Use external services |
| Function timeout (10s free, 60s pro) | Optimize code, use background jobs |

---

## 🎯 Vercel vs Other Platforms

| Feature | Vercel | Render | Railway |
|---------|--------|--------|---------|
| **Free Tier** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Flask Support** | ⚠️ Requires adaptation | ✅ Native | ✅ Native |
| **File Storage** | ❌ No (use cloud) | ⚠️ Ephemeral | ⚠️ Ephemeral |
| **Database** | ❌ External needed | ✅ Included | ✅ Included |
| **Cold Starts** | ⚠️ Yes | ❌ No | ❌ No |
| **Best For** | Frontend + API | Full-stack apps | Full-stack apps |

---

## 🚀 Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] `vercel.json` created
- [ ] `vercel_app.py` created (or `api/index.py`)
- [ ] Database connection updated for environment variables
- [ ] File uploads configured for cloud storage
- [ ] External database set up (PostgreSQL)
- [ ] Environment variables configured in Vercel
- [ ] Deployed to Vercel
- [ ] Database initialized
- [ ] Application tested

---

## 📚 Alternative: Use Vercel for Frontend Only

**Better approach for Flask apps:**

1. **Deploy Flask API on Render/Railway** (easier for Flask)
2. **Deploy frontend on Vercel** (if you separate frontend)
3. **Connect them via API**

This gives you:
- ✅ Best of both worlds
- ✅ Flask on proper platform
- ✅ Fast frontend on Vercel CDN

---

## 🆘 Need Help?

- **Vercel Docs:** [vercel.com/docs](https://vercel.com/docs)
- **Vercel Python:** [vercel.com/docs/python](https://vercel.com/docs/python)
- **Vercel Support:** [vercel.com/support](https://vercel.com/support)

---

## 💡 Recommendation

**For SmartHire Flask app, I recommend:**

1. **Use Render or Railway** for the full Flask app (easier setup)
2. **OR** if you want Vercel:
   - Separate frontend/backend
   - Deploy Flask API on Render
   - Deploy frontend on Vercel

**Vercel is great, but Render/Railway are easier for Flask apps!**

---

**Last Updated:** Vercel deployment guide for SmartHire

