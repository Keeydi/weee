# Render Setup - Troubleshooting "This action is not allowed"

## 🔴 Error: "This action is not allowed"

This error typically appears when:
1. ❌ GitHub repository is not connected
2. ❌ Required fields are missing
3. ❌ You need to scroll down to see more configuration options

---

## ✅ Solution Steps

### Step 1: Connect GitHub Repository First

**Before filling the form, you MUST connect your GitHub repository:**

1. Look for a section that says **"Connect Repository"** or **"Public Git Repository"**
2. If you see a button like **"Connect account"** or **"Connect GitHub"**, click it
3. Authorize Render to access your GitHub repositories
4. Select your repository: `Keeeeeeeeydi/smarthire`
5. **Then** come back to fill the form

**The repository connection is usually at the TOP of the form, before the name field.**

---

### Step 2: Complete All Required Fields

Make sure you fill in:

1. **Repository:** Should show `Keeeeeeeeydi/smarthire` (after connecting)
2. **Name:** `smarthire` ✅ (you have this)
3. **Region:** Singapore ✅ (you have this)
4. **Branch:** `main` ✅ (you have this)
5. **Root Directory:** Leave **EMPTY** ✅ (you have this)
6. **Build Command:** ⚠️ **YOU NEED THIS!**
   ```
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```
7. **Start Command:** ⚠️ **YOU NEED THIS!**
   ```
   gunicorn -c gunicorn_config.py wsgi:app
   ```

---

### Step 3: Scroll Down to See More Options

The form might have more sections below. **Scroll down** to see:
- Build Command field
- Start Command field
- Environment Variables section
- Advanced settings

---

### Step 4: Check Your Render Account

If the error persists:

1. **Verify your account is activated:**
   - Check your email for verification
   - Make sure you're logged in

2. **Check free tier limits:**
   - Free tier allows 1 web service
   - If you already have one, you might need to delete it first

3. **Try refreshing the page:**
   - Sometimes the form needs a refresh after connecting GitHub

---

## 📋 Complete Configuration Checklist

Use this checklist to ensure everything is filled:

- [ ] **GitHub Repository Connected** (most important!)
- [ ] Repository shows: `Keeeeeeeeydi/smarthire`
- [ ] Name: `smarthire`
- [ ] Region: Singapore (or same as your database)
- [ ] Branch: `main`
- [ ] Root Directory: **EMPTY** (leave blank)
- [ ] **Build Command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- [ ] **Start Command:** `gunicorn -c gunicorn_config.py wsgi:app`
- [ ] Environment variables added (after service is created)

---

## 🔍 Where to Find Build/Start Commands

The Build Command and Start Command fields are usually:
- **Below** the Root Directory field
- In a section labeled **"Build & Deploy"** or **"Build Settings"**
- Sometimes in an **"Advanced"** section

**Scroll down on the form to find them!**

---

## 🚀 Quick Fix Steps

1. **First:** Look for "Connect Repository" or "Public Git Repository" section
2. **Click:** Connect your GitHub account
3. **Select:** `Keeeeeeeeydi/smarthire` repository
4. **Then:** Fill in the rest of the form
5. **Scroll down:** Find Build Command and Start Command fields
6. **Fill them in:** Use the commands above
7. **Click:** "Deploy Web Service"

---

## ⚠️ Common Mistakes

1. ❌ Trying to deploy before connecting GitHub
2. ❌ Leaving Build Command empty
3. ❌ Leaving Start Command empty
4. ❌ Not scrolling down to see all fields
5. ❌ Using wrong branch name (should be `main`)

---

## 💡 Alternative: Use "Auto-Deploy" Option

If you're still having issues:

1. **Skip the manual form**
2. Go to your GitHub repository
3. Look for Render's **"Deploy to Render"** button (if available)
4. Or use Render's **"New from Template"** and connect your repo

---

## 🆘 Still Having Issues?

1. **Check Render Status:** [status.render.com](https://status.render.com)
2. **Contact Render Support:** Use the chat widget in Render dashboard
3. **Check Render Docs:** [render.com/docs](https://render.com/docs)

---

## ✅ Once It Works

After the service is created:

1. Go to your web service dashboard
2. Click **"Environment"** tab
3. Add environment variables:
   - `PYTHON_VERSION=3.11.0`
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - `DATABASE_URL=postgresql://...` (from your database)
   - Email settings (MAIL_*)

4. The service will automatically deploy!

---

**Most likely issue: You need to connect the GitHub repository first!** 🔗

