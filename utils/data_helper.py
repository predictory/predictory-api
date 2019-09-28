import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from db import db
from es.expert_system import ExpertSystem
from utils.recommendations_helper import RecommendationsHelper
from models.user_rating import UserRatingModel


class DataHelper:
    @staticmethod
    def load_data():
        users_ratings = db.session.query(UserRatingModel).all()
        users_ratings = [row.__dict__ for row in users_ratings]
        data = pd.DataFrame(users_ratings)
        n_users = data['userId'].unique().shape[0]
        n_items = data['movieId'].unique().shape[0]
        movies = data['movieId'].unique()
        users = data['userId'].unique()

        data_matrix = pd.DataFrame(np.zeros((n_users, n_items)), columns=movies, index=users)
        for line in data.itertuples():
            data_matrix.at[line.userId, line.movieId] = line.rating

        return csr_matrix(data_matrix, dtype=np.float32), movies, users

    @staticmethod
    def prepare_cbf_data(user_id, num_of_rated_items, ratings, take=10, skip=0, genres=None):
        if ratings is not None and num_of_rated_items > 0:
            recommendations = RecommendationsHelper.get_recommendations(ratings, take * 2, skip, user_id, genres)
            recommendations = ExpertSystem.get_scores(user_id, recommendations)
            recommendations = recommendations[:take]
        else:
            recommendations = ratings

        return recommendations

    @staticmethod
    def pack_recommendations_for_response(user_id, recommendations, num_of_rated_items, num_of_ratings):
        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations
        }

        return recommendations
