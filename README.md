# 🔒 PIPPF - Pre-Indexing Phishing Detection Framework

**A B.Tech Final Year Project** - Web-based phishing detection system using machine learning.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- Git

### Development Setup

```bash
# Backend
cd backend/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 📁 Project Structure

```
pippf-project-updated/
├── backend/              # Django REST API
│   └── backend/         # Main Django project
│       ├── manage.py
│       ├── requirements.txt
│       └── [apps...]    # analysis, api, core_api, crawler, decision, notification
│
├── frontend/            # React.js application
│   ├── src/
│   ├── public/
│   └── package.json
│
└── Ml-Model/           # ML models and prediction
    └── predict/
```

---

## 🌐 Deployment

### Option 1: Heroku + Netlify (Recommended)

**Backend on Heroku:**
```bash
cd backend/backend
heroku login
heroku create your-app-name
git push heroku main
```

**Frontend on Netlify:**
```bash
cd frontend
npm run build
# Upload 'build' folder to Netlify
```

### Option 2: Docker
```bash
docker-compose up -d
```

### Option 3: VPS (AWS/DigitalOcean)
See documentation in repository.

---

## 🔧 Configuration

Create `.env` in `backend/backend/`:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pippf_db
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## 📚 Features

✅ URL analysis and phishing detection  
✅ Machine learning classification  
✅ Real-time verification  
✅ Admin dashboard  
✅ REST API  
✅ Responsive frontend  

---

## 🧪 Testing

```bash
# Backend tests
cd backend/backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

---

## 🔐 Security

- Django security middleware enabled
- CSRF protection
- CORS configured
- SSL/TLS in production
- Environment variables for secrets

---

## 📖 Documentation

- See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions
- See `QUICK_DEPLOYMENT.md` for quick reference

---

## 👨‍💻 Tech Stack

**Backend:**
- Django 6.0.3
- Django REST Framework 3.16.1
- PostgreSQL/SQLite

**Frontend:**
- React 18.2.0
- Tailwind CSS 3.3.0
- Axios for API calls

**ML:**
- scikit-learn
- pandas
- numpy

---

## 📊 Project Status

- ✅ Backend API complete
- ✅ Frontend application complete
- ✅ ML models integrated
- ✅ Database configured
- ✅ Deployment ready

---

## 📞 Support

For issues or questions, check:
1. Terminal/console error messages
2. Django logs: `python manage.py check`
3. Browser console (F12)
4. GitHub issues

---

**Last Updated:** April 2026  
**Repository:** https://github.com/12214614/Pre-indexing-phishing-detection-framework
