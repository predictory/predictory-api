import time
import pandas as pd
from flask_restful import fields, marshal
from mongo import mongo
from db import db

from models.user_rating import UserRatingModel
from models.movie import MovieModel

rating_fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}


class SVDRecommender:
    @staticmethod
    def recommend(user_id, k=10):
        start = time.time()

        mongo_ratings = mongo.db.users_ratings
        rated_movies = marshal(UserRatingModel.query.filter_by(userId=user_id).all(), fields)

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
        recommended_movies = dict(ratings[:k])
        recommendations = [{'id': key, 'rating': float(value)} for key, value in recommended_movies.items()]

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        num_of_rated_items = len(user_rated_movies)
        return num_of_rated_items, recommendations

    @staticmethod
    def recommend_by_genre(user_id, genre_id, k=10):
        start = time.time()

        mongo_ratings = mongo.db.users_ratings
        rated_movies = marshal(UserRatingModel.query.filter_by(userId=user_id).all(), rating_fields)
        genre_movies = db.session.query(MovieModel.id).join(MovieModel.genres).filter_by(id=genre_id).all()

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

        user_row = dict((k, v) for k, v in user_row.items() if int(k) in genre_movies)
        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])
        recommended_movies = dict(ratings[:k])
        recommendations = [{'id': key, 'rating': float(value)} for key, value in recommended_movies.items()]

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return num_of_rated_items, recommendations
