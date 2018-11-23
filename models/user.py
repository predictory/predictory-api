from db import db

from models.user_rating import UserRatingModel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.string(100))
    password = db.Column(db.string(100))
    admin = db.Column(db.Boolean)
    ratings = db.relationship('UserRatingModel', backref='user', lazy=True)
