from datetime import datetime
from app.database import db, CRUDMixin
from app.supremum.models import Supremum


class Infimum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supremum_id = db.Column(db.Integer, db.ForeignKey(
        'supremum.id'), nullable=False)
    content = db.Column(db.String(), nullable=False, unique=True)
    submission_date = db.Column(db.DateTime, nullable=False)
    rejected = db.Column(db.Boolean, nullable=False)

    def __init__(self, supremum_id, content, submission_date=None, rejected=False, **kwargs):
        super(Infimum, self).__init__(**kwargs)
        self.supremum_id = supremum_id,
        self.content = content
        if submission_date is None:
            self.submission_date = datetime.now()
        else:
            self.submission_date = submission_date
        self.rejected = rejected

    def __repr__(self):
        return f'<Infimum #{self.id}>'

    def __dict__(self):
        return {
            'id': self.id,
            'supremum_id': self.supremum_id,
            'content': self.content,
            'submission_date': self.submission_date,
            'rejected': self.rejected
        }
