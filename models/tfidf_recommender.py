import time
from mongo import mongo


class TFIDFRecommender:
    def recommend(self, movie_id, k=10):
        start = time.time()

        mongo_similarities = mongo.db.tfidf_similarities
        similarities = mongo_similarities.find_one({'id': movie_id})

        end = time.time()
        print(f'Recommended in: {end - start} s')

        if similarities is None:
            return None

        return similarities['similarities'][:k]
