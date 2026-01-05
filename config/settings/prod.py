from .base import *

DEBUG = False
ALLOWED_HOSTS = ['furniturestore-production-abbc.up.railway.app',
    '.up.railway.app',]  # Change this in production

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
