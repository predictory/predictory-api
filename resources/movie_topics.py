from flask_restful import Resource
from models.lda_recommender import LDARecommender


class MovieTopics(Resource):
    @staticmethod
    def get(movie_id):
        recommender = LDARecommender()

        return {
            'movieId': movie_id,
            'topics': recommender.get_movie_topics(movie_id).tolist()
        }, 200
