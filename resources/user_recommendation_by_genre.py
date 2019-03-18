from flask_restful import Resource
from recommenders.cbf_recommender import CBFRecommender


class UserRecommendationByGenre(Resource):
    @staticmethod
    def get(user_id, genre_id):
        recommendations = CBFRecommender.get_recommendations_by_genre(user_id, genre_id, 10)
        return recommendations, 200
