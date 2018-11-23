import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
from flask_restful import fields, marshal
from models.user_rating import UserRatingModel

fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}

class CBFRecommender():
    @staticmethod
    def get_recommendations(user_id):
        recommendations = CBFRecommender.svd(user_id, 10)
        return recommendations

    @staticmethod
    def svd(user, n):
        users_ratings = marshal(UserRatingModel.query.all(), fields)
        data = pd.DataFrame(users_ratings)
        n_users = data['userId'].unique().shape[0]
        n_items = data['movieId'].unique().shape[0]
        users = data['userId'].unique()
        movies = data['movieId'].unique()

        data_matrix = pd.DataFrame(np.zeros((n_users, n_items)), columns=movies, index=users)
        for line in data.itertuples():
           data_matrix.at[line.userId, line.movieId] = line.rating

        data_matrix_mean = np.mean(data_matrix.values, axis=1)
        data_matrix_demeaned = data_matrix.values - data_matrix_mean.reshape(-1, 1)
        U, sigma, Vt = svds(data_matrix_demeaned, k=20)
        sigma = np.diag(sigma)

        predicted_ratings = pd.DataFrame(np.dot(np.dot(U, sigma), Vt) + data_matrix_mean.reshape(-1, 1), columns = movies, index = users)

        user_movies = pd.DataFrame(data_matrix.loc[user])
        user_movies.columns = ['rating']
        viewed_movies = user_movies[user_movies['rating'] > 0].index
        predicted_movies_ratings = pd.DataFrame(predicted_ratings.loc[user])
        predicted_movies_ratings.columns = ['rating']
        recommended_movies = predicted_movies_ratings.drop(viewed_movies).sort_values(['rating'], ascending=[0]).head(n)
        recommendations = {
            'userId': user,
            'recommendations': [{index: line.rating} for index, line in recommended_movies.iterrows()]
        }

        return recommendations

    @staticmethod
    def ib(user, n):
        metric = 'cosine'

        users_ratings = marshal(UserRatingModel.query.all(), fields)
        data = pd.DataFrame(users_ratings)
        n_users = data['userId'].unique().shape[0]
        n_items = data['movieId'].unique().shape[0]
        users = data['userId'].unique()
        movies = data['movieId'].unique()

        data_matrix = pd.DataFrame(np.zeros((n_users, n_items)), columns=movies, index=users)
        for line in data.itertuples():
           data_matrix.at[line.userId, line.movieId] = line.rating

        item_similarity = 1 - pairwise_distances(data_matrix.transpose(), metric=metric)

        pred = data_matrix.values.dot(item_similarity) / np.array([np.abs(item_similarity).sum(axis=1)])
        item_prediction = pd.DataFrame(pred, columns = movies, index = users)

        user_movies = pd.DataFrame(data_matrix.loc[user])
        user_movies.columns = ['rating']
        viewed_movies = user_movies[user_movies['rating'] > 0].index
        predicted_ratings = pd.DataFrame(item_prediction.loc[user])
        predicted_ratings.columns = ['rating']
        recommended_movies = predicted_ratings.drop(viewed_movies).sort_values(['rating'], ascending=[0]).head(n)
        recommendations = {
            'userId': user,
            'recommendations': [{index: line.rating} for index, line in recommended_movies.iterrows()]
        }

        return recommendations

    @staticmethod
    def ub(user, n):
        metric = 'cosine'

        users_ratings = marshal(UserRatingModel.query.all(), fields)
        data = pd.DataFrame(users_ratings)
        n_users = data['userId'].unique().shape[0]
        n_items = data['movieId'].unique().shape[0]
        users = data['userId'].unique()
        movies = data['movieId'].unique()

        data_matrix = pd.DataFrame(np.zeros((n_users, n_items)), columns=movies, index=users)
        for line in data.itertuples():
           data_matrix.at[line.userId, line.movieId] = line.rating

        user_similarity = 1 - pairwise_distances(data_matrix, metric=metric)

        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        user_prediction = pd.DataFrame(pred, columns = movies, index = users)

        user_movies = pd.DataFrame(data_matrix.loc[user])
        user_movies.columns = ['rating']
        viewed_movies = user_movies[user_movies['rating'] > 0].index
        predicted_ratings = pd.DataFrame(item_prediction.loc[user])
        predicted_ratings.columns = ['rating']
        recommended_movies = predicted_ratings.drop(viewed_movies).sort_values(['rating'], ascending=[0]).head(n)
        recommendations = {
            'userId': user,
            'recommendations': [{index: line.rating} for index, line in recommended_movies.iterrows()]
        }

        return recommendations
