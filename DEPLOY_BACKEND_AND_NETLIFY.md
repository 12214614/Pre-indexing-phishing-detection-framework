Backend + Netlify Deployment Steps

1. Deploy backend on Render
- Go to Render dashboard.
- Create New + Blueprint.
- Select this repository.
- Render will detect render.yaml at repository root.
- Service root is phishing_backend/backend.

2. Set backend environment variables in Render
- DJANGO_SECRET_KEY = strong random secret
- DJANGO_DEBUG = False
- DJANGO_ALLOWED_HOSTS = your-backend-domain.onrender.com
- DJANGO_ENABLE_CSRF = True
- DJANGO_CORS_ALLOW_ALL_ORIGINS = False
- DJANGO_CORS_ALLOWED_ORIGINS = https://preindexingphishingframework.netlify.app
- DJANGO_CSRF_TRUSTED_ORIGINS = https://preindexingphishingframework.netlify.app
- DJANGO_CORS_ALLOW_CREDENTIALS = True

3. Confirm backend URL
- Example: https://your-backend-domain.onrender.com
- Health check endpoint: https://your-backend-domain.onrender.com/api/core/dashboard/

4. Configure Netlify frontend environment variable
- In Netlify Site settings, open Environment variables.
- Add:
  REACT_APP_API_BASE_URL = https://your-backend-domain.onrender.com/api/core

5. Trigger Netlify redeploy
- In Netlify, open Deploys.
- Select Clear cache and deploy site.

6. Verify end-to-end
- Open https://preindexingphishingframework.netlify.app
- Go to Verify URL page.
- Submit a test URL.
- If API fails, check browser console network tab and Render logs.
