"""
Vercel serverless function entry point for SmartHire Flask application.
This file is used by Vercel to handle all requests.
"""
from app import app

# Export the Flask app as the handler for Vercel
handler = app

