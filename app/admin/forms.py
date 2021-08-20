from flask_wtf import Form
from wtforms import BooleanField, StringField, FileField, IntegerField, DateField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from app.home.models import Infimum


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
            "type":"number",
            "min":"0"
        }
    )
    edition_nr = IntegerField(
        'Edition nr.',
        validators=[DataRequired()],
        render_kw={
            "type":"number",
            "min":"0",
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
        if kwargs.get("prepopulate", False):
            self.supremum = kwargs.get("supremum", {})
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

class InfimumEditForm(Form):
    infimum_id = IntegerField(
        'Infimum id',
        validators=[DataRequired()],
        render_kw = {
            "type":"number",
            'disabled': True # read-only field
        }
    )
    supremum = SelectField(
        'Supremum', coerce=int
    )
    content = StringField(
        'Theme',
        validators=[DataRequired()],
        widget=TextArea()
    )
    creation_date = DateField(
        'Submission date',
        validators = [DataRequired()],
        render_kw = {
            'disabled': True # read-only field
        }
    )
    rejected = BooleanField(
        'Rejected'
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if kwargs.get("prepopulate", False):
            infimum = kwargs.get("infimum", {})
            self.infimum_id.data = infimum.get("id", '')
            self.content.data = infimum.get('content', '')
            self.creation_date.data = infimum.get('submission_date', '')
            self.rejected.data = infimum.get('rejected', False)

            self.supremum.choices = kwargs.get("suprema", []) + [(-1, "Not selected")]
            self.supremum.data = infimum.get("supremum_id", None) or -1

    def _check_types(self):
        valid = True

        if not isinstance(self.content.data, str):
            self.content.errors.append('Infimum must consist of text.')
            valid = False

        print(self.rejected.data)
        if not isinstance(self.rejected.data, bool):
            self.rejected.errors.append('Rejected must be a boolean.')
            valid = False

        return valid


    def validate(self):
        rv = Form.validate(self)
        if not self._check_types():
            return False
        return True

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class InfimumAssignForm(Form):
    supremum = SelectField('Supremum edition')
    infima = MultiCheckboxField('Infima', coerce=int)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        infima = kwargs.get("infima", [])
        self.infima.choices = [(i['id'], i['content']) for i in infima]

        suprema = kwargs.get("suprema", [])
        self.supremum.choices = [(sup.id, str(sup)) for sup in suprema]

    def validate(self):
        return True
