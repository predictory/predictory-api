import time
from utils.recommendations_helper import RecommendationsHelper
from utils.database_helper import DatabaseHelper


class SVDRecommender:
    @staticmethod
    def recommend(user_id):
        start = time.time()

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)

        if len(rated_movies) == 0:
            return 0, 0, None

        user_row = RecommendationsHelper.get_user_movies(rated_movies, user_id)

        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings

    @staticmethod
    def recommend_by_genre(user_id, genres_ids, movie_type=None, include_rated=False):
        start = time.time()

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)

        if len(rated_movies) == 0:
            return 0, 0, None

        genre_movies = DatabaseHelper.get_movies_by_genres_and_type(genres_ids, movie_type)

        if len(genre_movies) == 0:
            return len(rated_movies), 0, None

        user_row = RecommendationsHelper.get_user_movies(rated_movies, user_id, include_rated)

        user_row = dict((k, user_row[str(k)]) for k in genre_movies if str(k) in user_row)
        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings
