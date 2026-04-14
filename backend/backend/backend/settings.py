"""
Django settings for backend project.
Development configuration for API usage.
"""

import os
from pathlib import Path


def env_bool(name, default=False):
    value = os.getenv(name, str(default)).strip().lower()
    return value in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]

# Base Directory

BASE_DIR = Path(__file__).resolve().parent.parent


# Security Settings

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key')

DEBUG = env_bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = env_list(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost' if DEBUG else ''
)

ENABLE_CSRF = env_bool('DJANGO_ENABLE_CSRF', not DEBUG)


# Installed Apps

INSTALLED_APPS = [
    # Default Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local Apps
    'crawler',
    'analysis',
    'decision',
    'notification',
    'core_api',
]


# Middleware

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if ENABLE_CSRF:
    MIDDLEWARE.insert(4, 'django.middleware.csrf.CsrfViewMiddleware')


# URLs

ROOT_URLCONF = 'backend.urls'


# Templates (kept for admin panel)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'backend.wsgi.application'


# Database (SQLite)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password Validation

AUTH_PASSWORD_VALIDATORS = []


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static Files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST Framework Settings
# Allow all APIs (No authentication required)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

CORS_ALLOW_ALL_ORIGINS = env_bool('DJANGO_CORS_ALLOW_ALL_ORIGINS', DEBUG)
CORS_ALLOWED_ORIGINS = env_list(
    'DJANGO_CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000,http://localhost:5000'
)
CSRF_TRUSTED_ORIGINS = env_list(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000,http://localhost:5000'
)
CORS_ALLOW_CREDENTIALS = env_bool('DJANGO_CORS_ALLOW_CREDENTIALS', True)
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
