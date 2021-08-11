from flask_wtf import Form
from wtforms import BooleanField, StringField, FileField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from app.infima.models import Infimum


class SupremumForm(Form):
    supremum_id = IntegerField(
        'Supremum id',
        render_kw = {
            "type":"number",
            'disabled': True # read-only field
        }
    )
    volume_nr = IntegerField(
        'Volume nr.',
        validators=[DataRequired()],
        render_kw={
            "type":"number"
        }
    )
    edition_nr = IntegerField(
        'Edition nr.',
        validators=[DataRequired()],
        render_kw={
            "type":"number",
            "max":"3"
        }
    )
    theme = StringField(
        'Theme',
        validators=[DataRequired()]
    )
    published = BooleanField(
        'Publish'
    )
    magazine = FileField(
        'Magazine .pdf',
        render_kw={"accept": ".pdf"}
    )
    cover = FileField(
        'Magazine cover',
        render_kw={"accept": "image/*"}
    )    

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.supremum = kwargs.get("supremum", {})
        print(self.supremum.get("volume_nr", ''))
        if self.supremum:
            self.supremum_id.data = self.supremum.get('id', None)
            self.volume_nr.data = self.supremum.get("volume_nr", '')
            self.edition_nr.data = self.supremum.get("edition_nr", '')
            self.theme.data = self.supremum.get("theme", '')
            self.published.data = self.supremum.get("published", '')

    def _check_types(self):
        valid = True
        volume_nr = self.volume_nr.data
        if not isinstance(volume_nr, int):
            self.volume_nr.errors.append('Volume nr. must be an integer.')
            valid = False
        
        edition_nr = self.edition_nr.data
        if not isinstance(edition_nr, int):
            self.edition_nr.errors.append('Edition nr. must be an integer.')
            valid = False
            
        theme = self.theme.data
        if not isinstance(theme, str):
            self.theme.errors.append('Theme must be text.')
            valid = False

        return valid
        

    def validate(self):
        rv = Form.validate(self)
        if not self._check_types():
            return False
        return True
 