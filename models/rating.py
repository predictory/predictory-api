from db import db


class RatingModel(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    value = db.Column(db.String(10))
    movieId = db.Column(db.Integer, db.ForeignKey('movies.id'))

    def __init__(self, source, value, movie_id):
        self.source = source
        self.value = value
        self.movieId = movie_id
