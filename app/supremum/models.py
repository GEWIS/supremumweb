from app.database import db, CRUDMixin


class Supremum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume_nr = db.Column(db.Integer, nullable=False)
    edition_nr = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(), nullable=False)
    filename_pdf = db.Column(db.String())
    filename_cover = db.Column(db.String())
    published = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Supremum #{self.id}>'

    def __str__(self):
        return f'Supremum {self.volume_nr}.{self.edition_nr} - {self.theme}'

    def format_public(self):
        return {
            'self': f"/supremum/{self.id}",
            'id': self.id,
            'volume_nr': self.volume_nr,
            'edition_nr': self.edition_nr,
            'theme': self.theme
        }

    def format_private(self):
        return {
            'self': f"/supremum/{self.id}",
            'id': self.id,
            'volume_nr': self.volume_nr,
            'edition_nr': self.edition_nr,
            'theme': self.theme,
            'published': self.published
        }

    @classmethod
    def get_supremum_by_id(cls, id: int):
        """Returns the supremum with the specified id or None if this does not exist"""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_supremum_by_volume_and_edition(cls, volume_nr: int, edition_nr: int):
        """Returns the supremum with the specified volume and edition nr, or None if this does not exist"""
        return cls.query.filter_by(volume_nr=volume_nr, edition_nr=edition_nr).first()

    @classmethod
    def get_all_published_editions(cls):
        """Returns a list containing all editions"""
        return cls.query.filter_by(published=True).all()

    @classmethod
    def _get_all_editions(cls):
        """Returns a list containing all editions"""
        return cls.query.all()
