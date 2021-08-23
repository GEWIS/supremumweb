from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from app.home.models import Infimum


class SubmitInfimumForm(Form):
    """Form used in submitting new infima"""

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

        infimum = Infimum.query.filter_by(
            content=self.infimum_text.data).first()

        if infimum:
            self.infimum.errors.append(
                'This infimum has already been submitted'
            )
            return False

        self.infimum = infimum
        return True


class InfimumSearchForm(Form):
    """Form used in searching for infima based on their content"""

    search_term = TextField(
        'search_term',
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Search for...',
            'autocomplete': 'off',
        }
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.term = None
