from db import db

from models.genre import GenreModel
from models.actor import ActorModel
from models.language import LanguageModel
from models.country import CountryModel
from models.rating import RatingModel

genres = db.Table('movies_genres',
    db.Column('moviesId', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('genresId', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

actors = db.Table('movies_actors',
    db.Column('moviesId', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actorsId', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)

languages = db.Table('movies_languages',
    db.Column('moviesId', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('languagesId', db.Integer, db.ForeignKey('languages.id'), primary_key=True)
)

countries = db.Table('movies_countries',
    db.Column('moviesId', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('countriesId', db.Integer, db.ForeignKey('countries.id'), primary_key=True)
)

class MovieModel(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    imdbId = db.Column(db.String(100))
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.String(5))
    releaseDate = db.Column(db.Date)
    genres = db.relationship('GenreModel', secondary=genres, lazy='subquery',
        backref=db.backref('movies', lazy=True))
    director = db.Column(db.String(100))
    actors = db.relationship('ActorModel', secondary=actors, lazy='subquery',
        backref=db.backref('movies', lazy=True))
    plot = db.Column(db.Text)
    languages = db.relationship('LanguageModel', secondary=languages, lazy='subquery',
        backref=db.backref('movies', lazy=True))
    countries = db.relationship('CountryModel', secondary=countries, lazy='subquery',
        backref=db.backref('movies', lazy=True))
    poster = db.Column(db.String(100))
    type = db.Column(db.String(50))
    production = db.Column(db.String(100))
    ratings = db.relationship('RatingModel', backref='movie', lazy=True)
