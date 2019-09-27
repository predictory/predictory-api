import time
from mongo import mongo


class LDARecommender:
    @staticmethod
    def recommend(movie_id, k=10):
        start = time.time()

        mongo_similarities = mongo.db.similarities
        similarities = mongo_similarities.find_one({'id': movie_id})

        end = time.time()
        print(f'Recommended in: {end - start} s')

        if similarities is None:
            return None

        return similarities['similarities'][:k]

    @staticmethod
    def get_movie_topics(movie_id):
        mongo_topics = mongo.db.topics
        movie_topics = mongo_topics.find_one({'id': movie_id})

        if movie_topics is None:
            return None

        return movie_topics['topics']
