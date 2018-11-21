from flask_restful import Resource
from recommenders.cb_recommender import CBRecommender

class MovieRecommendation(Resource):
    def get(self, id):
        recommendations = CBRecommender.get_recommendations(id)
        return recommendations, 200
