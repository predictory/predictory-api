from flask_restful import Resource
from flask import request
from recommenders.cbf_recommender import CBFRecommender


class UserRecommendation(Resource):
    @staticmethod
    def get(user_id):
        genres = request.args.get('genres')
        movie_type = request.args.get('type')
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        order_by = request.args.get('order_by', 'rating,es_score')
        order_by = order_by.split(',')

        recommendations = CBFRecommender.get_recommendations(user_id, take, skip, genres, movie_type, order_by=order_by)
        return recommendations, 200
