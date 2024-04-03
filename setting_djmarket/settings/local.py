from  .base import *
from .db import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['ravasquez.pythonanywhere.com','localhost', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = DB_SQLITE3
