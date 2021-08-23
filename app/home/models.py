from flask import current_app
from sqlalchemy.sql.functions import random
from sqlalchemy.sql.expression import func
from app.database import db, CRUDMixin

import os
import random
import math
from typing import List

class Supremum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume_nr = db.Column(db.Integer, nullable=False)
    edition_nr = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(), nullable=False)
    filename_pdf = db.Column(db.String())
    filename_cover = db.Column(db.String())
    published = db.Column(db.Boolean, nullable=False)

    @property
    def self(self):
        return f"/supremum/{self.id}"

    @property
    def pdf_url(self):
        if self.filename_cover:
            return os.path.join('/', current_app.config['DATA_PATH'], self.filename_pdf)
        return None

    @property
    def cover_url(self):
        if self.filename_cover:
            return os.path.join('/', current_app.config['DATA_PATH'], self.filename_cover)
        return None

    def __str__(self):
        return f'Supremum {self.volume_nr}.{self.edition_nr} - {self.theme}'

    def __repr__(self):
        return f'Supremum(id={self.id}, volume_nr={self.volume_nr}, '\
            f'edition_nr={self.edition_nr}, theme="{self.theme}", '\
            f'filename_pdf="{self.filename_pdf}", '\
            f'filename_cover="{self.filename_cover})", '\
            f'published={self.published})'

    @classmethod
    def get_by_volume_and_edition(cls, volume_nr: int, edition_nr: int):
        """Returns the supremum with the specified volume and edition nr, or None if this does not exist"""
        return cls.query.filter_by(volume_nr=volume_nr, edition_nr=edition_nr).first()

    @classmethod
    def get_published_editions(cls):
        """Returns a list containing all editions"""
        return cls.query.filter_by(published=True).all()

    @classmethod
    def get_published_editions_in_order(cls):
        """Returns all published editions, ordered from newest to oldest"""
        return cls.query\
            .filter_by(published=True)\
            .order_by(Supremum.volume_nr.desc(), Supremum.edition_nr.desc())\
            .all()

    @classmethod
    def get_latest_published_edition(cls):
        """Returns the published edition with the highest volume and edition nr"""
        try:
            return cls.get_published_editions_in_order()[0]
        except:
            return None

    @classmethod
    def _get_editions(cls):
        """Returns a list containing all editions"""
        return cls.query.all()

    @classmethod
    def _get_editions_in_order(cls):
        """Returns a list containing all editions, with most recent first."""
        return cls.query\
            .order_by(Supremum.volume_nr.desc(), Supremum.edition_nr.desc())\
            .all()


class Infimum(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supremum_id = db.Column(db.Integer, db.ForeignKey('supremum.id'),
                            nullable=False)
    content = db.Column(db.String(), nullable=False, unique=True)
    submission_date = db.Column(db.DateTime, nullable=False)
    rejected = db.Column(db.Boolean, nullable=False)

    @property
    def self(self):
        return "/supremum/{}.{}/infima#{}".format(self.supremum.volume_nr,
                                                  self.supremum.edition_nr,
                                                  self.id)

    @property
    def supremum(self):
        return Supremum.get_by_id(self.supremum_id)

    @property
    def volume_nr(self):
        return self.supremum.volume_nr if self.supremum else None

    @property
    def edition_nr(self):
        return self.supremum.edition_nr if self.supremum else None

    @property
    def theme(self):
        return self.supremum.theme if self.supremum else None

    def __repr__(self):
        return f'Infimum(id={self.id}, '\
            f'supremum_id={self.supremum_id}, '\
            f'content="{self.content}", '\
            f'submission_date={repr(self.submission_date)}, '\
            f'rejected={self.rejected})'

    def format_public(self):
        return {
            "self": self.self,
            "id": self.id,
            "content": self.content,
            "volume_nr": self.volume_nr,
            "edition_nr": self.edition_nr,
            "theme": self.theme
        }

    @classmethod
    def _search_infima(cls, search_term: str) -> List:
        """Returns all infima whose content contain the search term."""
        filter = cls.content.like(f'%{search_term}%')
        return cls.query.filter(filter).filter_by(rejected=False).all()

    # TODO: make this query more efficient using some form of (right?)-join
    @classmethod
    def search_published_infima(cls, search_term: str) -> List:
        """Returns all published, non-rejected infima whose content contain the search term."""

        search_results = cls._search_infima(search_term)
        published_suprema = Supremum.get_published_editions()
        published_suprema_ids = [sup.id for sup in published_suprema]

        filtered_results = [
            inf for inf in search_results
            if inf.supremum_id in published_suprema_ids
        ]
        return filtered_results

    @classmethod
    def get_infima_with_supremum_id(cls, id):
        return cls.query.filter_by(supremum_id=id).all()

    @classmethod
    def get_random_infimum(cls, depth=0):
        # Stop after too many searches
        if depth == 10:
            return None

        # Choose supremum edition, favoring recently released suprema
        published_suprema = Supremum.get_published_editions()
        if not published_suprema:
            return None
        RANDOM_BASE = current_app.config['RANDOM_BASE']
        rand_int = random.randint(1, RANDOM_BASE ** len(published_suprema))
        rand_idx = math.floor(math.log(rand_int, RANDOM_BASE)) - 1
        supremum = published_suprema[::-1][rand_idx]

        # Get random non-rejected infimum from random supremum
        random_infimum = Infimum.query\
            .filter_by(supremum_id=supremum.id, rejected=False)\
            .order_by(func.random()).first()

        # Return infimum, or try again if None was found.
        return random_infimum or cls.get_random_infimum(depth + 1)

    @classmethod
    def _get_unassigned_infima(cls):
        return cls.query.filter_by(supremum_id=None).all()

    @classmethod
    def get_infimum_with_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_infimum_with_content(cls, content):
        return cls.query.filter_by(content=content).first()
