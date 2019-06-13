import time
from flask_restful import fields, marshal
from db import db
from sqlalchemy import func

from models.user_rating import UserRatingModel
from models.movie import MovieModel
from models.genre import GenreModel
from utils.recommendations_helper import RecommendationsHelper

rating_fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}


class SVDRecommender:
    @staticmethod
    def recommend(user_id):
        start = time.time()

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)

        if len(rated_movies) == 0:
            return 0, None

        user_row = RecommendationsHelper.get_user_movies(rated_movies, user_id)

        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings

    @staticmethod
    def recommend_by_genre(user_id, genres_ids, movie_type=None, include_rated=False):
        start = time.time()

        rated_movies = marshal(UserRatingModel.query.filter_by(userId=user_id).all(), rating_fields)
        genre_movies = db.session.query(MovieModel.id).join(MovieModel.genres)

        if movie_type is not None:
            genre_movies = genre_movies.filter(MovieModel.type == movie_type)

        genre_movies = genre_movies.filter(GenreModel.id.in_(genres_ids))\
            .group_by(MovieModel.id)\
            .having(func.count(GenreModel.id) == len(genres_ids)).all()

        if len(rated_movies) == 0:
            return 0, None

        if len(genre_movies) == 0:
            return len(rated_movies), None

        genre_movies = [movie[0] for movie in genre_movies]

        user_row = RecommendationsHelper.get_user_movies(rated_movies, user_id, include_rated)

        user_row = dict((k, user_row[str(k)]) for k in genre_movies if str(k) in user_row)
        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings
