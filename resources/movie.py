from flask_restful import Resource, fields, marshal_with

from models.movie import MovieModel

genres_fields = {
    'id': fields.Integer,
    'name': fields.String
}

ratings_fields = {
    'source': fields.String,
    'value': fields.String
}

movies_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'type': fields.String,
    'genres': fields.List(fields.Nested(genres_fields)),
    'ratings': fields.List(fields.Nested(ratings_fields))
}

class Movie(Resource):
    @marshal_with(movies_fields)
    def get(self):
        movies = MovieModel.query.limit(5).all()
        return movies, 200
