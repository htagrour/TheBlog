import os
from datetime import timedelta
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or "db"
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or 'root'
    MYSQL_DB = os.environ.get("MYSQL_DB") or 'tinder_clone'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    PERMANENT_SESSION_LIFETIME = timedelta(days =7)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ['my_email@gmail.com']