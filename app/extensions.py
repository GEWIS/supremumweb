from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache

fbcrypt = Bcrypt()
lm = LoginManager()
cache = Cache(config={'CACHE_TYPE': "simple"})