from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache
from flask_cors import CORS

fbcrypt = Bcrypt()
lm = LoginManager()
cache = Cache(config={'CACHE_TYPE': "simple"})
cors = CORS(
    origins=['gewis.nl', '*.gewis.nl', 'win.tue.nl',
             '*.win.tue.nl', 'localhost:8080'],
    resources=[r'/api/*']
)
