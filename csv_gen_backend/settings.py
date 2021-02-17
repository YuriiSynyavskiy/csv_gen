"""
Django settings for csv_gen_backend project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import boto3
from redis import Redis, from_url
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost',
                 'https://csv-gen-planeks.herokuapp.com/', 'csv-gen-planeks.herokuapp.com']
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'csv_gen',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'csv_gen_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'csv_gen_backend.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
# Redis
SECRET_KEY = '1^wjxg_-8b!9vk*yvsx$^%%7d2d%ywp2&en2joz%p0fh@@3)f5'

# Celery
redis_host = os.environ.get('REDIS_HOST', 'localhost')
REDIS_CONN = from_url(os.environ['REDIS_URL']) if os.environ.get(
    'REDIS_URL', None) else Redis(host=redis_host, port=os.environ.get('REDIS_PORT', 6379))
CELERY_BROKER_URL = os.environ.get(
    'REDIS_URL', None) or f'redis://{redis_host}:6379'
CELERY_RESULT_BACKEND = os.environ.get(
    'REDIS_URL', None) or f'redis://{redis_host}:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

"""

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', None) or 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % {
        'user': os.environ['POSTGRES_USER'],
        'pw': os.environ['POSTGRES_PASSWORD'],
        'db': os.environ['POSTGRES_DB'],
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': '5432',
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', ""),
        'USER': os.environ.get('POSTGRES_USER', ""),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ""),
        'HOST': 'localhost',
        'PORT': '5432',  # default port
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'https://master.d2bxryo6wqbzm8.amplifyapp.com',
]
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
DATASETS_ROOT = 'datasets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
S3_CLIENT = boto3.client('s3')
