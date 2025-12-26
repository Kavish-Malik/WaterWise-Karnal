from pathlib import Path

import os

import mimetypes

from django.utils.translation import gettext_lazy as _



import dj_database_url







# Now you can safely use os.getenv()

API_KEY = os.getenv('API_KEY')



# Base directory

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ["SECRET_KEY"]





DEBUG = True



ALLOWED_HOSTS = [

    "waterwise-karnal.onrender.com",

    ".onrender.com",

    "127.0.0.1",

    "localhost",

]







# Installed apps

INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',



    'django.contrib.sites',            # ✅ Required for allauth

    'allauth',                         # ✅ Core allauth

    'allauth.account',                 # ✅ Email/account system

    'allauth.socialaccount',           # ✅ Social login

    'allauth.socialaccount.providers.google',  # ✅ Google login



    'members',                         # Your app

]



SITE_ID = 1



# Auth backends

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',

]



# AllAuth settings

LOGIN_REDIRECT_URL = '/dashboard/'

LOGOUT_REDIRECT_URL = '/'



ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_AUTHENTICATION_METHOD = 'username'

ACCOUNT_EMAIL_REQUIRED = False

SOCIALACCOUNT_QUERY_EMAIL = True



SOCIALACCOUNT_PROVIDERS = {

    'google': {

        'APP': {

            'client_id': os.getenv('GOOGLE_CLIENT_ID'),

            'secret': os.getenv('GOOGLE_SECRET'),  # fixed to match .env

            'key': ''

        }

    }

}



# Middleware

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Static file handling

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware', 

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'allauth.account.middleware.AccountMiddleware',  # ✅ Optional for better allauth support

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]



# URLs

ROOT_URLCONF = 'water.urls'



# Templates

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'members' / 'templates'],  # ✅ Matches your structure

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.debug',

                'django.template.context_processors.request',  # ✅ Needed for allauth

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]



WSGI_APPLICATION = 'water.wsgi.application'



DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is NOT set at runtime")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
    )
}













# Password validation

AUTH_PASSWORD_VALIDATORS = [

    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},

    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},

    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},

    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},

]



# Internationalization

LANGUAGE_CODE = 'en-us'  # Removed duplicate LANGUAGE_CODE



TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JS, fonts)

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# Ensure fonts are served correctly

mimetypes.add_type("application/font-woff", ".woff", True)

mimetypes.add_type("application/font-woff2", ".woff2", True)



# Default primary key field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



SOCIALACCOUNT_AUTO_SIGNUP = True

ACCOUNT_SIGNUP_REDIRECT_URL = '/dashboard/'

SOCIALACCOUNT_ADAPTER = 'members.adapter.MySocialAccountAdapter'



USE_I18N = True



LANGUAGES = [

    ('en', _('English')),

    ('hi', _('Hindi')),

]



LOCALE_PATHS = [

    BASE_DIR / 'locale',

]











CSRF_TRUSTED_ORIGINS = [

    "https://waterwise-karnal.onrender.com",

    "https://www.waterwise-karnal.onrender.com",

]

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True



