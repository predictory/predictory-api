import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from db import db
from models.user_rating import UserRatingModel


class DatabaseHelper:
    @staticmethod
    def load_data_matrix():
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
    def get_movies_by_genres_and_type(genres_ids, movie_type):
        print('genres')
