from db import db
import enum


class TopGenreType(enum.Enum):
    MOST_RATED = 'most-rated'
    MOST_VALUED = 'most-valued'
    LEAST_RATED = 'least_rated'
    LEAST_VALUED = 'least_valued'


class LimitType(enum.Enum):
    TOP_THREE = 'top-three'
    TOP_TWELVE = 'top-twelve'


class TopGenre(db.Model):
    __tablename__ = 'topGenres'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    genreId = db.Column(db.Integer, db.ForeignKey('genres.id'))
    value = db.Column(db.Integer)
    genreType = db.Column(db.String)
    genreLimit = db.Column(db.String)
