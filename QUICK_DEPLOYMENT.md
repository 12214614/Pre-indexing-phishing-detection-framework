# ⚡ QUICK DEPLOYMENT REFERENCE

## 🎯 When You're Ready to Deploy

### 1️⃣ LOCAL TESTING (Before Deploy)
```bash
# Stop current servers if running (Ctrl+C)

# Backend
cd backend/backend
python manage.py check
python manage.py test

# Frontend  
cd frontend
npm run build  # Should complete without errors
```

### 2️⃣ PUSH TO GITHUB
```bash
git add .
git commit -m "Ready for production"
git push origin main
```

### 3️⃣ CHOOSE YOUR DEPLOYMENT OPTION

#### 🟢 EASIEST: Heroku + Netlify (5 minutes)

**Backend on Heroku:**
```bash
cd backend/backend
heroku login
heroku create your-app-name
git push heroku main
heroku config:set DJANGO_DEBUG=False DJANGO_SECRET_KEY=your-secret
```

**Frontend on Netlify:**
- Build: `npm run build`
- Upload `frontend/build/` folder to Netlify
- Set environment variables in Netlify dashboard
- Done! ✅

#### 🟡 MEDIUM: AWS/DigitalOcean VPS (30 minutes)

**Quick Setup:**
```bash
# 1. SSH into VPS
ssh ubuntu@your-server-ip

# 2. Install & Setup Backend
sudo apt update && sudo apt install -y python3.11 python3-pip nodejs npm nginx postgresql
git clone <your-repo>
cd Pre-indexing-phishing-detection-framework/backend/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
sudo nano .env  # Add your config
python manage.py migrate
python manage.py collectstatic --noinput

# 3. Build Frontend
cd ../../frontend
npm install && npm run build

# 4. Setup Process Manager
sudo apt install supervisor
sudo nano /etc/supervisor/conf.d/pippf.conf
# Paste config from DEPLOYMENT_GUIDE.md

# 5. Setup Reverse Proxy
sudo apt install nginx
sudo nano /etc/nginx/sites-available/pippf
# Paste config from DEPLOYMENT_GUIDE.md
sudo systemctl restart nginx

# 6. SSL Certificate
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

#### 🔴 ADVANCED: Docker (20 minutes)

Create `docker-compose.yml` in root:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: pippf_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend/backend
    command: >
      sh -c "python manage.py migrate &&
             gunicorn backend.wsgi:application --bind 0.0.0.0:8000"
    environment:
      DJANGO_DEBUG: "False"
      DJANGO_SECRET_KEY: "your-secret-key"
      DB_ENGINE: django.db.backends.postgresql
      DB_NAME: pippf_db
      DB_USER: postgres
      DB_PASSWORD: password
      DB_HOST: db
      DB_PORT: 5432
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./backend/backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app

volumes:
  postgres_data:
```

```bash
docker-compose up -d
# Done! Backend: http://localhost:8000, Frontend: http://localhost:3000
```

---

## 📋 CHECKLIST BEFORE GOING LIVE

- [ ] Database configured (SQLite OK for small apps, PostgreSQL for production)
- [ ] `.env` file created with production settings
- [ ] `DJANGO_DEBUG = False`
- [ ] HTTPS/SSL enabled (critical for security)
- [ ] CORS configured for your frontend domain
- [ ] ALLOWED_HOSTS configured
- [ ] Logging configured
- [ ] Backups automated
- [ ] Monitoring set up
- [ ] Error alerts configured

---

## 🔐 CRITICAL SECURITY SETTINGS

```env
# .env file (NEVER commit this!)

# 1. Secret Key (generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DJANGO_SECRET_KEY=your-50-char-random-key

# 2. Disable Debug
DJANGO_DEBUG=False

# 3. Allowed Hosts
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 4. CORS Origins
CORS_ALLOWED_ORIGINS=https://your-domain.com

# 5. HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# 6. Database Credentials (use PostgreSQL in production!)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pippf_db
DB_USER=pippf_user
DB_PASSWORD=strong-password
DB_HOST=your-db-host
DB_PORT=5432
```

---

## 🚨 COMMON PROBLEMS & FIXES

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'django'` | Activate venv: `source .venv/bin/activate` |
| `TemplateDoesNotExist` | Run: `python manage.py collectstatic --noinput` |
| `ProgrammingError` when accessing API | Run: `python manage.py migrate` |
| Port 8000/3000 already in use | Kill process: `lsof -ti:8000 \| xargs kill -9` |
| CORS errors in browser console | Update CORS_ALLOWED_ORIGINS in .env |
| Static files (CSS/JS) not loading | Run: `python manage.py collectstatic --noinput --clear` |
| Database connection error | Check DB credentials in .env |

---

## 📊 POST-DEPLOYMENT MONITORING

```bash
# Check if backend is running
curl http://your-domain.com/api/

# Check if frontend loads
curl http://your-domain.com/

# View logs
sudo tail -f /var/log/pippf/error.log
sudo tail -f /var/log/pippf/access.log

# Monitor resources
htop

# Check processes
sudo supervisorctl status pippf
```

---

## 🔄 HOW TO UPDATE PRODUCTION

```bash
# 1. Make changes locally
# 2. Test thoroughly
# 3. Commit and push
git add .
git commit -m "Fix: description"
git push origin main

# 4. SSH into server
ssh ubuntu@your-server-ip

# 5. Pull changes
cd Pre-indexing-phishing-detection-framework
git pull origin main

# 6. Backend updates
cd backend/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart pippf

# 7. Frontend updates
cd ../../frontend
npm install
npm run build
# Copy build files to Nginx root or redeploy

# 8. Verify
curl https://your-domain.com/api/
```

---

## 💾 DATABASE BACKUP

```bash
# SQLite (simple)
cp backend/backend/db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# PostgreSQL (full)
pg_dump -U pippf_user pippf_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore PostgreSQL
psql -U pippf_user pippf_db < backup_20260414.sql
```

---

## 📞 EMERGENCY CONTACTS

If something breaks in production:

1. **Check logs**: `sudo tail -f /var/log/pippf/error.log`
2. **Restart backend**: `sudo supervisorctl restart pippf`
3. **Restart Nginx**: `sudo systemctl restart nginx`
4. **Rollback**: `git revert <commit-hash> && git push`

---

**Remember**: Test locally before deploying to production! 🚀
