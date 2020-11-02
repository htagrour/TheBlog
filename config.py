import os
from datetime import timedelta
class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or "localhost"
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'hamza'
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or '1234'
    MYSQL_DB = os.environ.get("MYSQL_DB") or 'my_blog'
    PERMANENT_SESSION_LIFETIME = timedelta(days =7)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ['my_email@gmail.com']