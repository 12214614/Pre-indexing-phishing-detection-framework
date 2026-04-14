# 🚀 PIPPF - Complete Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Development Deployment](#development-deployment)
4. [Production Deployment](#production-deployment)
5. [Database Setup](#database-setup)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.10+** (verify: `python --version`)
- **Node.js 16+** (verify: `node --version`)
- **npm 8+** (verify: `npm --version`)
- **Git** (verify: `git --version`)

### Required Services (for Production)
- **PostgreSQL 12+** (recommended for production, or keep SQLite)
- **Nginx** or **Apache** (for reverse proxy)
- **Gunicorn** (WSGI server, already in requirements.txt)
- **Supervisor** or **systemd** (for process management)

---

## Environment Setup

### Step 1: Clone and Navigate
```bash
cd /e/pippf-project-updated
```

### Step 2: Create Virtual Environment (if not exists)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Create `.env` File
Create `.env` file in `/backend/backend/` directory with:

```env
# Django Settings
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here-min-50-chars
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com,www.your-domain.com

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# Database (optional – defaults to SQLite)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pippf_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Security
DJANGO_ENABLE_CSRF=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 4: Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Development Deployment

### Quick Start (What You Just Did)

```bash
# Terminal 1: Backend
cd backend/backend
pip install -r requirements.txt
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm install
npm start
```

**Access Points:**
- 🔗 Backend: `http://127.0.0.1:8000/`
- 🔗 Frontend: `http://localhost:3000/`

---

## Production Deployment

### Option A: Heroku Deployment (Easiest for Quick Deploy)

#### Backend Setup
1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Create `Procfile`** in `/backend/backend/`:
```
web: gunicorn backend.wsgi --log-file -
release: python manage.py migrate
```

3. **Create `runtime.txt`** in `/backend/backend/`:
```
python-3.11.8
```

4. **Deploy**:
```bash
cd backend/backend
heroku login
heroku create your-app-name
git push heroku main
heroku config:set DJANGO_DEBUG=False
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku open
```

#### Frontend Setup (Netlify)
1. **Build frontend**:
```bash
cd frontend
npm run build
```

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Create new site → Upload `./frontend/build/` folder
   - Set environment variables in Netlify

---

### Option B: VPS Deployment (AWS, DigitalOcean, etc.)

#### Step 1: Server Preparation
```bash
# SSH into your VPS
ssh ubuntu@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3-pip nodejs npm nginx postgresql postgresql-contrib supervisor git
```

#### Step 2: Backend Setup
```bash
# Clone repository
git clone https://github.com/12214614/Pre-indexing-phishing-detection-framework.git
cd Pre-indexing-phishing-detection-framework/backend/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see Environment Setup section)
nano .env

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Test run
python manage.py runserver 0.0.0.0:8000
```

#### Step 3: Frontend Build
```bash
cd ../../frontend
npm install
npm run build

# Output will be in ./build/ directory
```

#### Step 4: Configure Gunicorn
Create `/home/ubuntu/gunicorn_config.py`:
```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2
```

#### Step 5: Configure Supervisor
Create `/etc/supervisor/conf.d/pippf.conf`:
```ini
[program:pippf]
directory=/home/ubuntu/Pre-indexing-phishing-detection-framework/backend/backend
command=/home/ubuntu/Pre-indexing-phishing-detection-framework/backend/backend/venv/bin/gunicorn \
    --config /home/ubuntu/gunicorn_config.py \
    backend.wsgi:application
user=ubuntu
autostart=true
autorestart=true
stderr_logfile=/var/log/pippf/error.log
stdout_logfile=/var/log/pippf/access.log
```

```bash
# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start pippf
```

#### Step 6: Configure Nginx
Create `/etc/nginx/sites-available/pippf`:
```nginx
upstream pippf_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Frontend
    root /home/ubuntu/Pre-indexing-phishing-detection-framework/frontend/build;
    index index.html;

    # Static files
    location /static/ {
        alias /home/ubuntu/Pre-indexing-phishing-detection-framework/backend/backend/staticfiles/;
    }

    # Backend API
    location /api/ {
        proxy_pass http://pippf_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin panel
    location /admin/ {
        proxy_pass http://pippf_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # React app (SPA routing)
    location / {
        try_files $uri /index.html;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/pippf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 7: SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

---

## Database Setup

### Development (SQLite - Default)
```bash
cd backend/backend
python manage.py migrate
python manage.py createsuperuser
```

### Production (PostgreSQL)

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE pippf_db;
CREATE USER pippf_user WITH PASSWORD 'strong_password';
ALTER ROLE pippf_user SET client_encoding TO 'utf8';
ALTER ROLE pippf_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pippf_user SET default_transaction_deferrable TO ON;
ALTER ROLE pippf_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pippf_db TO pippf_user;
\q

# Update .env with PostgreSQL credentials
# Then run migrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Complete Deployment Checklist

### Before Deployment

- [ ] Update `.env` file with production values
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Generate strong `DJANGO_SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
- [ ] Set up database (PostgreSQL recommended)
- [ ] Enable SSL/TLS (HTTPS)
- [ ] Run `python manage.py check` to verify configuration
- [ ] Run tests: `python manage.py test`
- [ ] Test frontend build: `npm run build`

### During Deployment

- [ ] Push code to GitHub
- [ ] Run migrations on production server
- [ ] Collect static files
- [ ] Run Gunicorn with Supervisor
- [ ] Configure Nginx reverse proxy
- [ ] Test backend API endpoints
- [ ] Test frontend application
- [ ] Check logs for errors

### After Deployment

- [ ] Monitor logs: `tail -f /var/log/pippf/error.log`
- [ ] Monitor processes: `sudo supervisorctl status pippf`
- [ ] Monitor server resources: `htop`
- [ ] Set up automated backups
- [ ] Configure uptime monitoring
- [ ] Set up alerting for errors

---

## Useful Commands

### Django Management
```bash
# Migrations
python manage.py migrate
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test

# Check configuration
python manage.py check

# Shell
python manage.py shell
```

### Supervisor
```bash
# View status
sudo supervisorctl status

# Start/Stop/Restart
sudo supervisorctl start pippf
sudo supervisorctl stop pippf
sudo supervisorctl restart pippf

# View logs
sudo tail -f /var/log/pippf/error.log
sudo tail -f /var/log/pippf/access.log
```

### Nginx
```bash
# Test configuration
sudo nginx -t

# Restart
sudo systemctl restart nginx

# View logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

---

## Troubleshooting

### Backend Issues

**Port already in use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database errors**
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Import errors**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use**
```bash
# Use different port
npm start -- --port 3001
```

**Dependencies issues**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build failure**
```bash
# Check build
npm run build

# Check for errors
npm audit
npm audit fix
```

### Deployment Issues

**Migrations not applied**
```bash
python manage.py migrate --run-syncdb
```

**Static files not loading**
```bash
python manage.py collectstatic --noinput --clear
```

**CORS errors**
```bash
# Update settings.py CORS settings
# Ensure frontend domain is in CORS_ALLOWED_ORIGINS
```

---

## Monitoring & Maintenance

### Server Health Check
```bash
# CPU and Memory
free -h
df -h

# Running processes
ps aux | grep python

# Network connections
netstat -tuln | grep 8000
```

### Regular Maintenance
```bash
# Update packages (Django, etc.)
pip install --upgrade -r requirements.txt

# Update Node packages
npm audit fix

# Database backup
pg_dump pippf_db > backup_$(date +%Y%m%d).sql

# Log rotation (Nginx/Supervisor handle automatically)
```

---

## Support & Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **React Docs**: https://react.dev/
- **Nginx Docs**: https://nginx.org/en/docs/
- **Gunicorn Docs**: https://gunicorn.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Last Updated**: April 2026
**Project**: Pre-Indexing Phishing Detection Framework
