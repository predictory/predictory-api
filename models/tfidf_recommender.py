import time
from mongo import mongo
from utils.database_helper import DatabaseHelper


class TFIDFRecommender:
    @staticmethod
    def recommend(movie_id, k=10, genres=None, movie_type=None):
        start = time.time()

        mongo_similarities = mongo.db.tfidf_similarities
        similarities = mongo_similarities.find_one({'id': movie_id})

        end = time.time()
        print(f'Recommended in: {end - start} s')

        if similarities is None:
            return None

        similarities = similarities['similarities']
        if genres is not None:
            genres_ids = genres.split(',')
            genre_movies = DatabaseHelper.get_movies_by_genres_and_type(genres_ids, movie_type)

            if len(genre_movies) == 0:
                return None

            similarities = [item for item in similarities if item['id'] in genre_movies]

        return similarities
