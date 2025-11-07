"""
Gunicorn configuration file for production deployment.
Adjust these settings based on your server resources.
"""
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"  # Change port if needed (check with Hostinger)
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1  # Formula: (2 x CPU cores) + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "logs/access.log"  # Create logs directory first
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "smarthire"

# Server mechanics
daemon = False
pidfile = "gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if you have SSL certificate)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

