"""
Django settings for DomoPhone project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9lxg5(2c(suq(ah!2-m)1o)y@an)nlq575@xz(py27cc-d0&u#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#AUTH_USER_MODEL = 'main.User'
ALLOWED_HOSTS = ["192.168.1.101", "127.0.0.1", "127.0.1.1"]


# Application definition
INSTALLED_APPS = [
    'main',
    'users',
    'own',
    'settings',
    'm_rfid',
    'm_finger',

    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# CronTab
CRONJOBS = [
    ("* * * * *", 'm_finger.module.Finger_loop', '>> /var/log/crontab/finger_loop.log'),
    #("* * * * *", 'main.cron.Rfid_loop', '>> /var/log/crontab/rfid_loop.log'),
    ("* * * * *", 'm_rfid.module.Rfid_loop', '>> /var/log/crontab/rfid_loop.log'),
    #("* * * * *", 'main.cron.RF_loop', '>> /var/log/crontab/rf_loop.log'),
    #("* * * * *", 'main.cron.Init_loop', '>> /var/log/crontab/time_loop.log')
]
WSGI_APPLICATION = 'DomoPhone.wsgi.application'
CRONTAB_COMMAND_SUFFIX = '2>&1'
CRONTAB_LOCK_JOBS = True



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'DomoPhone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

"""
CELERY_BEAT_SCHEDULE = {
    'example-task': {
        'task': 'Main.tasks.test',
        'schedule': 5,  # в секундах, или timedelta(seconds=10)
    },
}
"""


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/', '/static/')
