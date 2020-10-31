import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from db import db
from models.user_rating import UserRatingModel
from models.movie import MovieModel
from models.genre import GenreModel
from models.top_genre import TopGenre, TopGenreType, LimitType
from sqlalchemy import func


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
    def load_data_matrix_limited_by_top_genres(user_id):
        user_top_genres = db.session.query(TopGenre)\
            .filter_by(userId=user_id)\
            .filter(db.or_(TopGenre.genreType==TopGenreType.MOST_VALUED.value, TopGenre.genreType==TopGenreType.LEAST_VALUED.value))\
            .filter_by(genreLimit=LimitType.TOP_THREE.value).all()

        most_valued_genres = [row.genreId for row in user_top_genres if row.genreType == TopGenreType.MOST_VALUED.value]
        least_valued_genres = [row.genreId for row in user_top_genres if row.genreType == TopGenreType.LEAST_VALUED.value]

        similar_users_most_valued = db.session.query(TopGenre.userId)\
            .filter(TopGenre.genreId.in_(most_valued_genres))\
            .filter(TopGenre.genreType == TopGenreType.MOST_VALUED.value)\
            .filter(TopGenre.genreLimit == LimitType.TOP_THREE.value) \
            .group_by(TopGenre.userId) \
            .having(func.count(TopGenre.userId) >= 2).all()
        most_valued_ids = [value for value, in similar_users_most_valued]
        similar_users_least_valued = db.session.query(TopGenre.userId) \
            .filter(TopGenre.genreId.in_(least_valued_genres)) \
            .filter(TopGenre.genreType == TopGenreType.LEAST_VALUED.value) \
            .filter(TopGenre.genreLimit == LimitType.TOP_THREE.value) \
            .group_by(TopGenre.userId) \
            .having(func.count(TopGenre.userId) >= 1).all()
        least_valued_ids = [value for value, in similar_users_least_valued]

        intersection = list(set(most_valued_ids) & set(least_valued_ids))

        users_ratings = db.session.query(UserRatingModel).filter(UserRatingModel.userId.in_(intersection)).all()
        users_ratings = [row.__dict__ for row in users_ratings]
        data = pd.DataFrame(users_ratings)
        n_users = data['userId'].unique().shape[0]
        n_items = data['movieId'].unique().shape[0]
        movies = data['movieId'].unique()
        users = data['userId'].unique()

        data_matrix = pd.DataFrame(np.zeros((n_users, n_items)), columns=movies, index=users)
        for line in data.itertuples():
            data_matrix.at[line.userId, line.movieId] = line.rating

        return csr_matrix(data_matrix, dtype=np.float32), movies, users, most_valued_genres, least_valued_genres

    @staticmethod
    def get_movies_by_genres_and_type(genres_ids, movie_type):
        genre_movies = db.session.query(MovieModel.id).join(MovieModel.genres)

        if movie_type is not None:
            genre_movies = genre_movies.filter(MovieModel.type == movie_type)

        genre_movies = genre_movies.filter(GenreModel.id.in_(genres_ids)) \
            .group_by(MovieModel.id) \
            .having(func.count(GenreModel.id) == len(genres_ids)).all()

        if len(genre_movies) == 0:
            return genre_movies

        return [movie[0] for movie in genre_movies]

    @staticmethod
    def get_movies_for_genres(genres_ids):
        genre_movies = db.session.query(MovieModel.id).join(MovieModel.genres)

        genre_movies = genre_movies.filter(GenreModel.id.in_(genres_ids)) \
            .group_by(MovieModel.id) \
            .all()

        if len(genre_movies) == 0:
            return genre_movies

        return [movie[0] for movie in genre_movies]
