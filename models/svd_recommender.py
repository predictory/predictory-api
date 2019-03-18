import time
import pandas as pd
from flask_restful import fields, marshal
from mongo import mongo

from models.user_rating import UserRatingModel

fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}


class SVDRecommender:
    def recommend(self, user_id, k=10):
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
