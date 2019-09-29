import time
from flask_restful import fields
from db import db
from sqlalchemy import func

from models.movie import MovieModel
from models.genre import GenreModel
from utils.recommendations_helper import RecommendationsHelper


class UserBasedRecommender:
    @staticmethod
    def recommend(user_id, sim_type='cosine'):
        start = time.time()

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)

        if len(rated_movies) == 0:
            return 0, 0, None

        user_row = RecommendationsHelper.get_user_movies_custom_based(rated_movies, user_id,
                                                                      include_rated=False,
                                                                      rec_type='user-based',
                                                                      sim_type=sim_type)

        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings

    @staticmethod
    def recommend_by_genre(user_id, genres_ids, movie_type=None, include_rated=False, sim_type='cosine'):
        start = time.time()

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)

        if len(rated_movies) == 0:
            return 0, 0, None

        genre_movies = db.session.query(MovieModel.id).join(MovieModel.genres)

        if movie_type is not None:
            genre_movies = genre_movies.filter(MovieModel.type == movie_type)

        genre_movies = genre_movies.filter(GenreModel.id.in_(genres_ids))\
            .group_by(MovieModel.id)\
            .having(func.count(GenreModel.id) == len(genres_ids)).all()

        if len(genre_movies) == 0:
            return len(rated_movies), None

        genre_movies = [movie[0] for movie in genre_movies]

        user_row = RecommendationsHelper.get_user_movies_custom_based(rated_movies, user_id, include_rated,
                                                                      'user-based',
                                                                      sim_type)

        user_row = dict((k, user_row[k]) for k in genre_movies if k in user_row)
        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings
