# SECURITY WARNING: don't run with debug turned on in production!

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = False
ALLOWED_HOSTS = ['localhost', 'lengua-translator.herokuapp.com']

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
