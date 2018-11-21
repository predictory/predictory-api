from flask_restful import Resource
from recommenders.cbf_recommender import CBFRecommender

class UserRecommendation(Resource):
    def get(self, id):
        recommendations = CBFRecommender.get_recommendations(id)
        return recommendations, 200
