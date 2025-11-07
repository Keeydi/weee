#!/bin/bash
# SmartHire - Hostinger Deployment Script
# Run this script on your Hostinger server via SSH

echo "=========================================="
echo "SmartHire - Hostinger Deployment"
echo "=========================================="
echo ""

# Navigate to project directory
cd ~/public_html/smarthire || cd ~/domains/*/public_html/smarthire

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Gunicorn
echo "Installing Gunicorn..."
pip install gunicorn

# Download spaCy model
echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm || pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p static/uploads
mkdir -p static/screenings
mkdir -p uploads
mkdir -p resumes
mkdir -p screened_resumes

# Set permissions
echo "Setting permissions..."
chmod -R 755 static templates
chmod -R 777 uploads resumes static/uploads static/screenings

# Initialize database
echo "Initializing database..."
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
EOF

echo ""
echo "=========================================="
echo "Deployment preparation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test Gunicorn: gunicorn -c gunicorn_config.py wsgi:app"
echo "2. Setup PM2: pm2 start gunicorn --name smarthire -- -c gunicorn_config.py wsgi:app"
echo "3. Save PM2: pm2 save"
echo "4. Setup startup: pm2 startup"
echo ""

