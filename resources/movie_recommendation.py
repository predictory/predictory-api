from flask_restful import Resource
from recommenders.cb_recommender import CBRecommender


class MovieRecommendation(Resource):
    def get(self, movie_id):
        recommendations = CBRecommender.get_recommendations(movie_id, 10)
        return recommendations, 200
