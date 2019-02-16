from flask_restful import Resource
from recommenders.hybrid_recommender import HybridRecommender


class HybridRecommendation(Resource):
    def get(self, user_id, movie_id):
        recommendations = HybridRecommender.get_recommendations(user_id, movie_id, 10)
        return recommendations, 200
