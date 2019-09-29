import time
from utils.recommendations_helper import RecommendationsHelper
from utils.database_helper import DatabaseHelper


class ItemBasedRecommender:
    @staticmethod
    def recommend(user_id, sim_type='cosine'):
        start = time.time()

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)

        if len(rated_movies) == 0:
            return 0, 0, None

        user_row = RecommendationsHelper.get_user_movies_custom_based(rated_movies, user_id,
                                                                      include_rated=False,
                                                                      rec_type='item-based',
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

        genre_movies = DatabaseHelper.get_movies_by_genres_and_type(genres_ids, movie_type)

        if len(genre_movies) == 0:
            return len(rated_movies), 0, None

        user_row = RecommendationsHelper.get_user_movies_custom_based(rated_movies, user_id, include_rated,
                                                                      'item-based',
                                                                      sim_type)

        user_row = dict((k, user_row[k]) for k in genre_movies if k in user_row)
        ratings = sorted(user_row.items(), reverse=True, key=lambda kv: kv[1])

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        return len(rated_movies), len(ratings), ratings
