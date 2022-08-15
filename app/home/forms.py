from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from app.home.models import Infimum


class SubmitInfimumForm(Form):
    """Form used in submitting new infima"""

    content = StringField(
        'content',
        validators=[DataRequired()],
        widget=TextArea(),
        render_kw={
            'placeholder': 'Write your infimum here...',
            'autocomplete': 'off',
        })

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate_content(self, *args):
        content = self.content.data.strip()

        # Check for duplicates
        already_exists = Infimum.get_infimum_with_content(content)
        if already_exists:
            self.content.errors.append(
                'This infimum has already been submitted'
            )

        # Check the submission is not just spaces
        contains_non_spaces = bool(content)
        if not contains_non_spaces:
            self.content.errors.append(
                'Please enter non-spaces too.'
            )
        return not already_exists and contains_non_spaces

    def validate(self):
        return Form.validate(self)


class InfimumSearchForm(Form):
    """Form used in searching for infima based on their content"""

    search_term = StringField(
        'search_term',
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Search for...',
            'autocomplete': 'off',
        }
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate_search_term(self, *args):
        search_term = self.search_term.data.strip()

        # Check the submission is not just spaces
        if not bool(search_term):
            self.search_term.errors.append(
                'Make sure your search term contains non-space characters'
            )

        # Check submission has at least two characters
        if len(search_term) < 2:
            self.search_term.errors.append('Please enter a longer search term')
        return bool(search_term) and len(search_term) >= 2

    def validate(self):
        return Form.validate(self)
