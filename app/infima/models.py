from app.database import db, CRUDMixin


class Infimum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False, unique=True)

    def __init__(self, text, **kwargs):
        super(Infimum, self).__init__(**kwargs)
        self.text = text

    def __repr__(self):
        return f'<Infimum #{self.id}:{self.text}>'
