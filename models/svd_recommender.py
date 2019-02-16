import time
import pandas as pd
import pickle
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
    def __init__(self):
        self.U = SVDRecommender.load_pickle_file('./models/SVD/u')
        self.sigma = SVDRecommender.load_pickle_file('./models/SVD/sigma')
        self.Vt = SVDRecommender.load_pickle_file('./models/SVD/vt')

    @staticmethod
    def load_pickle_file(file_name):
        file = open(f'{file_name}.pickle', 'rb')
        object_file = pickle.load(file)
        return object_file

    def recommend(self, user_id, k=10):
        start = time.time()

        mongo_ratings = mongo.db.users_ratings
        rated_movies = marshal(UserRatingModel.query.filter_by(userId=user_id).all(), fields)

        if len(rated_movies) == 0:
            return 0, None

        user_rated_movies = list(map(str, pd.DataFrame(rated_movies)['movieId'].values))
        user_row = mongo_ratings.find_one({'id': user_id})
        user_ratings = pd.DataFrame(user_row['ratings'], index=[user_id]).T
        user_ratings.columns = ['rating']
        recommended_movies = user_ratings.drop(user_rated_movies).sort_values(['rating'], ascending=False).head(k)

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        recommendations = [{'id': index, 'rating': float(row.rating)} for index, row in recommended_movies.iterrows()]
        num_of_rated_items = len(user_rated_movies)
        return num_of_rated_items, recommendations
