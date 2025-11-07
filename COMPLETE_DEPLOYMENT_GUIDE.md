# 🚀 Complete SmartHire Deployment Guide - Hostinger VPS

**Step-by-step guide to deploy your entire SmartHire system from scratch.**

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- ✅ Hostinger VPS account with root access
- ✅ SSH access enabled
- ✅ Your SmartHire code ready (on GitHub or local)
- ✅ Domain name connected (optional, but recommended)

---

## 🎯 Complete Deployment Steps

### **PHASE 1: Prepare Your Server**

#### Step 1: Access SSH Terminal
1. Go to Hostinger hPanel → VPS → Your VPS
2. Click **"Terminal"** button
3. Or use SSH client: `ssh root@YOUR_SERVER_IP`

#### Step 2: Update System
```bash
apt update
apt upgrade -y
```

#### Step 3: Install Required Software
```bash
# Install Python and pip
apt install python3 python3-pip python3-venv -y

# Install MySQL
apt install mysql-server -y

# Install Node.js and npm (for PM2)
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Install Git
apt install git -y

# Install Nginx (web server)
apt install nginx -y
```

#### Step 4: Start Services
```bash
systemctl start mysql
systemctl enable mysql
systemctl start nginx
systemctl enable nginx
```

---

### **PHASE 2: Setup MySQL Database**

#### Step 5: Secure MySQL
```bash
mysql_secure_installation
```

Follow prompts:
- Set root password: **Yes** (choose a strong password)
- Remove anonymous users: **Yes**
- Disallow root login remotely: **Yes**
- Remove test database: **Yes**
- Reload privilege tables: **Yes**

#### Step 6: Create Database and User
```bash
mysql -u root -p
```

Enter your MySQL root password, then run:

```sql
-- Create database
CREATE DATABASE smarthire CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (replace 'StrongPassword123!' with your own)
CREATE USER 'smarthire_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';

-- Grant all privileges
GRANT ALL PRIVILEGES ON smarthire.* TO 'smarthire_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

**Save these credentials:**
- Database: `smarthire`
- Username: `smarthire_user`
- Password: `StrongPassword123!` (the one you set)
- Host: `localhost`

---

### **PHASE 3: Deploy Your Application**

#### Step 7: Navigate to Web Directory
```bash
cd /var/www
mkdir -p smarthire
cd smarthire
```

#### Step 8: Clone Your Repository
```bash
# Clone from GitHub
git clone https://github.com/Keeydi/SmartHire.git .

# OR if you need authentication:
git clone https://Keeydi:YOUR_GITHUB_TOKEN@github.com/Keeydi/SmartHire.git .
```

#### Step 9: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 10: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Install spaCy model
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

#### Step 11: Create Required Directories
```bash
mkdir -p logs
mkdir -p static/uploads
mkdir -p static/screenings
mkdir -p uploads
mkdir -p resumes
mkdir -p screened_resumes
```

#### Step 12: Set Permissions
```bash
chmod -R 755 static templates
chmod -R 777 uploads resumes static/uploads static/screenings logs
```

---

### **PHASE 4: Configure Application**

#### Step 13: Update app.py Configuration

Edit `app.py`:

```bash
nano app.py
```

**Update these 3 lines:**

**Line 30 - Database Connection:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://smarthire_user:StrongPassword123!@localhost/smarthire'
```
(Replace `StrongPassword123!` with your actual MySQL password)

**Line 25 - Secret Key:**
```python
app.secret_key = "your-very-long-random-secret-key-change-this-to-something-secure"
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Line 1566 - Debug Mode:**
```python
app.run(debug=False)
```

Save: `Ctrl+X`, then `Y`, then `Enter`

#### Step 14: Update Gunicorn Config

Edit `gunicorn_config.py`:

```bash
nano gunicorn_config.py
```

Update the bind address:
```python
bind = "127.0.0.1:8000"  # Keep this for Nginx reverse proxy
```

Save and exit.

---

### **PHASE 5: Initialize Database**

#### Step 15: Create Database Tables
```bash
# Make sure venv is activated
source venv/bin/activate

# Initialize database
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
EOF
```

---

### **PHASE 6: Setup Process Manager (PM2)**

#### Step 16: Install PM2
```bash
npm install -g pm2
```

#### Step 17: Start Application with PM2
```bash
cd /var/www/smarthire
source venv/bin/activate

# Start with PM2
pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
```

**Follow the command that `pm2 startup` gives you!** (Usually something like `sudo env PATH=...`)

#### Step 18: Check PM2 Status
```bash
pm2 list
pm2 logs smarthire
```

---

### **PHASE 7: Configure Nginx (Web Server)**

#### Step 19: Create Nginx Configuration

```bash
nano /etc/nginx/sites-available/smarthire
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;  # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/smarthire/static;
    }

    location /uploads {
        alias /var/www/smarthire/uploads;
    }
}
```

Save: `Ctrl+X`, then `Y`, then `Enter`

#### Step 20: Enable Nginx Site
```bash
# Create symbolic link
ln -s /etc/nginx/sites-available/smarthire /etc/nginx/sites-enabled/

# Remove default site (optional)
rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Reload Nginx
systemctl reload nginx
```

---

### **PHASE 8: Setup SSL Certificate (HTTPS)**

#### Step 21: Install Certbot
```bash
apt install certbot python3-certbot-nginx -y
```

#### Step 22: Get SSL Certificate
```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to get a free SSL certificate.

---

### **PHASE 9: Final Configuration**

#### Step 23: Configure Firewall (Optional but Recommended)
```bash
# Allow SSH
ufw allow 22/tcp

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable
```

#### Step 24: Test Your Application

1. Visit: `http://yourdomain.com` or `http://YOUR_SERVER_IP`
2. Test signup/login
3. Test file uploads
4. Check database connectivity

---

## ✅ Deployment Checklist

- [ ] Server updated and software installed
- [ ] MySQL installed and secured
- [ ] Database and user created
- [ ] Code cloned to `/var/www/smarthire`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Directories created and permissions set
- [ ] `app.py` configured (database, secret key, debug=False)
- [ ] Database tables initialized
- [ ] PM2 installed and application running
- [ ] Nginx configured and running
- [ ] SSL certificate installed (optional)
- [ ] Application tested and working

---

## 🐛 Troubleshooting

### Application not loading
```bash
# Check PM2
pm2 list
pm2 logs smarthire
pm2 restart smarthire

# Check Nginx
systemctl status nginx
nginx -t

# Check Gunicorn
ps aux | grep gunicorn
```

### Database connection error
```bash
# Test MySQL connection
mysql -u smarthire_user -p smarthire

# Check MySQL is running
systemctl status mysql
```

### Permission errors
```bash
chmod -R 755 /var/www/smarthire
chmod -R 777 /var/www/smarthire/uploads
chmod -R 777 /var/www/smarthire/logs
```

### Port already in use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process if needed
kill -9 PID
```

---

## 📊 Useful Commands

### PM2 Commands
```bash
pm2 list              # List all apps
pm2 logs smarthire    # View logs
pm2 restart smarthire # Restart app
pm2 stop smarthire    # Stop app
pm2 delete smarthire  # Remove from PM2
```

### MySQL Commands
```bash
mysql -u root -p                    # Login as root
mysql -u smarthire_user -p smarthire # Login as app user
```

### Nginx Commands
```bash
systemctl status nginx  # Check status
nginx -t                # Test configuration
systemctl reload nginx   # Reload configuration
systemctl restart nginx  # Restart Nginx
```

---

## 🔄 Updating Your Application

When you make changes:

```bash
cd /var/www/smarthire
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
pm2 restart smarthire
```

---

## 🎉 Success!

Your SmartHire application should now be:
- ✅ Running on your VPS
- ✅ Accessible via your domain
- ✅ Using MySQL database
- [ ] Protected with SSL (if you completed Step 22)
- ✅ Automatically starting on server reboot

**Your application URL:** `http://yourdomain.com` or `https://yourdomain.com`

---

## 📞 Need Help?

- **Check logs:** `pm2 logs smarthire`
- **Check Nginx:** `systemctl status nginx`
- **Check MySQL:** `systemctl status mysql`
- **Hostinger Support:** Contact via hPanel

---

**Follow these steps in order, and your system will be fully deployed!** 🚀

