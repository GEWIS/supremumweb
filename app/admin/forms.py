from flask import request
from flask_wtf import Form
from wtforms import BooleanField, StringField, FileField, IntegerField, DateField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets import TextArea

from app.home.models import Supremum

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
        validators=[InputRequired()],
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
        self.supremum = kwargs.get("supremum", None)
        if kwargs.get("prepopulate", False):
            self.supremum_id.data = self.supremum.id
            self.volume_nr.data = self.supremum.volume_nr
            self.edition_nr.data = self.supremum.edition_nr
            self.theme.data = self.supremum.theme
            self.published.data = self.supremum.published

    def validate_volume_nr(self, *args):
        volume_nr = self.volume_nr.data
        is_valid = isinstance(volume_nr, int)
        if not is_valid:
            self.volume_nr.errors.append('Volume nr. must be an integer.')
        return is_valid

    def validate_edition_nr(self, *args):
        edition_nr = self.edition_nr.data
        is_valid = isinstance(edition_nr, int)
        if not is_valid:
            self.edition_nr.errors.append('Edition nr. must be an integer.')
        return is_valid

    def validate_theme(self, *args):
        theme = self.theme.data
        is_valid = isinstance(theme, str)
        if not is_valid:
            self.theme.errors.append('Theme must be text.')
        return is_valid

    # TODO: validate file is actually pdf
    def validate_magazine(self, *args):
        magazine = request.files.getlist(self.magazine.name)
        is_valid = len(magazine) <= 1
        if not is_valid:
            self.magazine.errors.append("Upload at most one file")
        return is_valid

    # TODO: validate file is actually an image
    def validate_cover(self, *args):
        cover = request.files.getlist(self.cover.name)
        is_valid = len(cover) <= 1
        if not is_valid:
            self.cover.errors.append("Upload at most one file")
        return is_valid

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        # Verify that if set to published, both magazine and cover are present
        set_to_publish = self.published.data
        if set_to_publish:
            # Require a magazine
            magazine = request.files.getlist(self.magazine.name)[0]
            has_magazine = bool(magazine) or self.supremum and self.supremum.filename_pdf
            if not has_magazine:
                self.published.errors.append(
                    "A magazine must be uploaded before publishing."
                )
                return False

            cover = request.files.getlist(self.magazine.name)[0]
            has_cover = bool(cover) or self.supremum and self.supremum.filename_cover
            if not has_cover:
                self.published.errors.append(
                    "A cover must be uploaded before publishing."
                )
                return False

        # Verify that if volume_nr or edition_nr is changed, these values are not yet in use
        new_volume_nr = self.volume_nr.data
        new_edition_nr = self.edition_nr.data
        if self.supremum.volume_nr != new_volume_nr or \
            self.supremum.edition_nr != new_edition_nr:
            supremum = Supremum.get_by_volume_and_edition(
                new_volume_nr, new_edition_nr)
            if supremum is not None:
                self.edition_nr.errors.append('This combination of volume_nr '\
                    'and edition_nr is already in use.')
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

    def validate_content(self, *args):
        content = self.content.data.strip()
        is_str = isinstance(content, str)
        if not is_str:
            self.content.errors.append('Infimum must consist of text.')
        is_non_empty = bool(content)
        if not is_non_empty:
            self.content.errors.append('Infimum must consist of text.')
        return is_str and is_non_empty

    def validate_rejected(self, *args):
        rejected = self.rejected.data
        is_valid = isinstance(self.rejected.data, bool)
        if not is_valid:
            self.rejected.errors.append('Rejected must be a boolean.')
        return is_valid

    def validate(self):
        return Form.validate(self)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class InfimumAssignForm(Form):
    supremum = SelectField('Supremum edition')
    infima = MultiCheckboxField('Infima', coerce=int)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        infima = kwargs.get("infima", [])
        self.infima.choices = [(i.id, i.content) for i in infima]

        suprema = kwargs.get("suprema", [])
        self.supremum.choices = [(sup.id, str(sup)) for sup in suprema]

    def validate_infima(self, *args):
        infima_ids = self.infima.data
        is_valid = bool(infima_ids)
        if not is_valid:
            self.infima.errors.append('At least one infimum must be selected')
        return is_valid

    def validate(self):
        return Form.validate(self)
