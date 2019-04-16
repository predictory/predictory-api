import time
import pandas as pd
from flask_restful import fields, marshal
from mongo import mongo
from db import db
from sqlalchemy import func

from models.user_rating import UserRatingModel
from models.movie import MovieModel
from models.genre import GenreModel

rating_fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}


class SVDRecommender:
    @staticmethod
    def recommend(user_id, take=10, skip=0):
        start = time.time()

        mongo_ratings = mongo.db.users_ratings
        rated_movies = marshal(UserRatingModel.query.filter_by(userId=user_id).all(), rating_fields)

        if len(rated_movies) == 0:
            return 0, None

        user_rated_movies = list(map(str, pd.DataFrame(rated_movies)['movieId'].values))
        user_row = mongo_ratings.find_one({'id': user_id})
        user_row = user_row['ratings']

        for rated_movie in user_rated_movies:
            try:
                del user_row[rated_movie]
            except:
                print('Movie not found')

        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])
        recommended_movies = dict(ratings[skip:take])
        recommendations = [{'id': key, 'rating': float(value)} for key, value in recommended_movies.items()]

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        num_of_rated_items = len(user_rated_movies)
        return num_of_rated_items, recommendations

    @staticmethod
    def recommend_by_genre(user_id, genres_ids, movie_type=None, take=10, skip=0):
        start = time.time()

        mongo_ratings = mongo.db.users_ratings
        rated_movies = marshal(UserRatingModel.query.filter_by(userId=user_id).all(), rating_fields)
        genre_movies = db.session.query(MovieModel.id).join(MovieModel.genres)

        if movie_type is not None:
            genre_movies = genre_movies.filter(MovieModel.type == movie_type)

        genre_movies = genre_movies.filter(GenreModel.id.in_(genres_ids))\
            .group_by(MovieModel.id)\
            .having(func.count(GenreModel.id) == len(genres_ids)).all()

        if len(rated_movies) == 0:
            return 0, None

        num_of_rated_items = len(rated_movies)

        if len(genre_movies) == 0:
            return num_of_rated_items, None

        genre_movies = [movie[0] for movie in genre_movies]

        user_rated_movies = list(map(str, pd.DataFrame(rated_movies)['movieId'].values))
        user_row = mongo_ratings.find_one({'id': user_id})
        user_row = user_row['ratings']

        for movie in user_rated_movies:
            try:
                del user_row[movie]
            except:
                print('Movie not found')

        user_row = dict((k, user_row[str(k)]) for k in genre_movies if str(k) in user_row)
        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])
        recommended_movies = dict(ratings[skip:take])
        recommendations = [{'id': key, 'rating': float(value)} for key, value in recommended_movies.items()]

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return num_of_rated_items, recommendations
