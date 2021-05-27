from app.database import db, CRUDMixin


class Supremum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume_nr = db.Column(db.Integer, nullable=False)
    edition_nr = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(), nullable=False)
    filename_pdf = db.Column(db.String())
    filename_cover = db.Column(db.String())
    published = db.Column(db.Boolean, nullable=False)

    def __init__(self, volume_nr, edition_nr, theme, filename_pdf=None, filename_cover=None, published=False):
        super(Supremum, self).__init__()
        self.volume_nr = volume_nr
        self.edition_nr = edition_nr
        self.theme = theme
        self.filename_pdf = filename_pdf
        self.filename_cover = filename_cover
        self.published = published        

    def __repr__(self):
        return f'<Supremum #{self.id}>'
    
    def __dict__(self):
        return {
            'id': self.id,
            'volume_nr': self.volume_nr,
            'edition_nr': self.edition_nr,
            'theme': self.theme,
            'filename_pdf': self.filename_pdf,
            'filename_cover': self.filename_cover,
            'published': self.published
        }
