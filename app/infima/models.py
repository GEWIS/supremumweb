from sqlalchemy.sql.expression import func
from app.database import db, CRUDMixin
from app.supremum.models import Supremum
from typing import List


class Infimum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supremum_id = db.Column(db.Integer, db.ForeignKey('supremum.id'), nullable=False)
    content = db.Column(db.String(), nullable=False, unique=True)
    submission_date = db.Column(db.DateTime, nullable=False)
    rejected = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Infimum #{self.id}>'

    def format_public(self):
        supremum = Supremum.get_supremum_by_id(self.supremum_id)
        return {
            "self": f"/supremum/{self.supremum_id}/infima/{self.id}",
            "id": self.id,
            "content": self.content,
            "volume_nr": supremum.volume_nr if supremum else None,
            "edition_nr": supremum.edition_nr if supremum else None,
            "theme": supremum.theme if supremum else ''
        }

    def format_private(self):
        return {
            "self": f"/supremum/{self.supremum_id}/infima/{self.id}",
            "id": self.id,
            "supremum_id": self.supremum_id,
            "content": self.content,
            "submission_date": self.submission_date,
            "rejected": self.rejected
        }

    @classmethod
    def search(cls, search_term:str) -> List:
        """Returns all infima whose content contain the search term."""
        filter = cls.content.like(f'%{search_term}%')
        return cls.query.filter(filter).all()

    @classmethod
    def get_infima_with_supremum_id(cls, id):
        return cls.query.filter_by(supremum_id=id).all()

    @classmethod
    def get_random_infimum(cls):
        random_infimum = None
        attempts = 0
        while random_infimum is None and attempts < 10:
            attempts += 1
            # Choose random published supremum edition
            random_supremum = Supremum.query.filter_by(published=True).order_by(func.random()).first()
            if random_supremum is None:
                # There is no published supremum
                return None

            # Get random non-rejected infimum from random supremum edition
            random_infimum = Infimum.query.filter_by(supremum_id=random_infimum.id, rejected=False).order_by(func.random()).first()
        return random_infimum

    @classmethod
    def _get_all_unassigned_infima(cls):
        return cls.query.filter_by(supremum_id=None).all()

    @classmethod
    def get_infimum_with_id(cls, id):
        return cls.query.filter_by(id=id).first()