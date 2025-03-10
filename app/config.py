import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))


class base_config(object):
    """Default configuration options."""
    SITE_NAME = os.environ.get('APP_NAME', 'supremumweb')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:8080')

    # Database settings
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'goodhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', 9999)
    MYSQL_USER = os.environ.get('MYSQL_USER', 'gooduser')
    MYSQL_PASS = os.environ.get('MYSQL_PASS', 'goodpass')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'goodbname')
    MYSQL_SSL = os.environ.get('MYSQL_SSL', False)

    base_uri = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
        MYSQL_USER,
        MYSQL_PASS,
        MYSQL_HOST,
        MYSQL_PORT,
        MYSQL_DB
    )

    if MYSQL_SSL:
        # In Alpine the CA certificates are located in `/etc/ssl/certs/`.
        SQLALCHEMY_DATABASE_URI = f"{base_uri}?ssl_ca=/etc/ssl/certs/&ssl_check_hostname=true"
    else:
        SQLALCHEMY_DATABASE_URI = base_uri

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # NGINX should take care of this.
    DATA_PATH = os.environ.get('DATA_PATH', '../data/')

    # Random infimum selection base
    RANDOM_BASE = os.environ.get('RANDOM_BASE', 2.0)

    # Writer manual url
    WRITER_MANUAL_URL = os.environ.get('WRITER_MANUAL_URL', '')

    # Random infimum API-key
    INFIMUM_RETRIEVE_KEY = os.environ.get('INFIMUM_RETRIEVE_KEY')
    INFIMUM_POST_KEY = os.environ.get('INFIMUM_POST_KEY')

    # GEWIS API-key, used for logging in
    GEWIS_API_KEY = os.environ.get('GEWIS_API_KEY')
    GEWIS_API_APPID = os.environ.get('GEWIS_API_APPID')


class dev_config(base_config):
    """Development configuration options."""
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///../database/supremum.db"
    SERVER_NAME = None


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False
