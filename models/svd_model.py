import os
from flask_restful import fields, marshal
import numpy as np
import pandas as pd
import pickle
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

from models.user_rating import UserRatingModel

fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}


class SVDModel:
    def __init__(self):
        self.n_users = 0
        self.n_items = 0

    def load_data(self):
        users_ratings = marshal(UserRatingModel.query.all(), fields)
        data = pd.DataFrame(users_ratings)
        self.n_users = data['userId'].unique().shape[0]
        self.n_items = data['movieId'].unique().shape[0]
        movies = data['movieId'].unique()
        users = data['userId'].unique()

        data_matrix = pd.DataFrame(np.zeros((self.n_users, self.n_items)), columns=movies, index=users)
        for line in data.itertuples():
            data_matrix.at[line.userId, line.movieId] = line.rating

        return csr_matrix(data_matrix, dtype=np.float32), movies, users

    @staticmethod
    def _save_pickle_file(file_name, data):
        file_name = f'./models/SVD/{file_name}.pickle'
        mapping_file = open(file_name, 'wb')
        pickle.dump(data, mapping_file)
        mapping_file.close()

    @staticmethod
    def save(U, sigma, Vt, predicted_ratings, movies, users):
        if not os.path.exists('./models/SVD'):
            os.makedirs('./models/SVD')

        SVDModel._save_pickle_file('u', U)
        SVDModel._save_pickle_file('sigma', sigma)
        SVDModel._save_pickle_file('vt', Vt)
        ratings_df = pd.DataFrame(predicted_ratings, columns=movies, index=users)
        SVDModel._save_pickle_file('predicted_ratings', ratings_df)

    @staticmethod
    def train(data, k):
        print('Start training SVD model...')
        data_mean = np.mean(data, axis=1)
        data_demeaned = data - data_mean.reshape(-1, 1)
        U, sigma, Vt = svds(data_demeaned, k=k)
        sigma = np.diag(sigma)
        predicted_ratings = np.dot(np.dot(U, sigma), Vt) + data_mean.reshape(-1, 1)
        print('Finished training SVD model...')

        return U, sigma, Vt, predicted_ratings
