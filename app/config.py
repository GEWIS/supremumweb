import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class base_config(object):
    """Default configuration options."""
    SITE_NAME = os.environ.get('APP_NAME', 'supremumweb')

    SECRET_KEY = os.environ.get('SECRET_KEY', 'secrets')
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:8080')

    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'goodhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', 9999)
    MYSQL_USER = os.environ.get('MYSQL_USER', 'gooduser')
    MYSQL_PASS = os.environ.get('MYSQL_PASS', 'goodpass')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'goodbname')


    DATA_PATH = os.environ.get('DATA_PATH', 'data/')
    RANDOM_BASE = os.environ.get('RANDOM_BASE', 2.0)

    # Random infimum API-key
    INFIMUM_API_KEY = os.environ.get('INFIMUM_API_KEY')


class dev_config(base_config):
    """Development configuration options."""
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False
