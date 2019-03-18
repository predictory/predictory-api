from flask_restful import Resource
from recommenders.cbf_recommender import CBFRecommender


class UserRecommendation(Resource):
    @staticmethod
    def get(user_id):
        recommendations = CBFRecommender.get_recommendations(user_id, 10)
        return recommendations, 200
