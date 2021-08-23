from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from app.auth.models import User

class LoginForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired()],
        render_kw= {
            'placeholder': 'Username'
        }
    )

    password = PasswordField(
        'password',
        validators=[DataRequired()],
        render_kw = {
            'placeholder': 'Password'
        }
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)

        self.user = User.query.filter_by(username=self.username.data).first()

        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True