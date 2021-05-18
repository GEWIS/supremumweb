from flask_login import UserMixin

from app.database import db, CRUDMixin
from app.extensions import fbcrypt


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    pw_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(password)

    def __repr__(self):
        return f'<User #{self.id}:{self.username}>'

    def set_password(self, password):
        hash_ = fbcrypt.generate_password_hash(password, 10).decode('utf-8')
        self.pw_hash = hash_

    def check_password(self, password):
        return fbcrypt.check_password_hash(self.pw_hash, password)