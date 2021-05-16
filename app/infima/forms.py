from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from app.infima.models import Infimum


class SubmitForm(Form):
    infimum_text = StringField(
        'infimum_text', 
        validators=[DataRequired()],
        widget=TextArea(),
        render_kw={
            'placeholder': 'Write your infimum here...',
            'autocomplete': 'off',
            })

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.infimum = None

    def validate(self):
        rv = Form.validate(self)

        infimum = Infimum.query.filter_by(text=self.infimum_text.data).first()

        if infimum:
            self.infimum.errors.append(
                'This infimum has already been submitted'
            )
            return False

        self.infimum = infimum
        return True
