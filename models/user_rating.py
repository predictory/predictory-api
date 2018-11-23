from db import db

class UserRatingModel(db.Model):
    __tablename__ = 'users_ratings'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    movieId = db.Column(db.Integer, db.ForeignKey('movies.id'))
    createdAt = db.Column(db.DateTime)
    rating = db.Column(db.Float)