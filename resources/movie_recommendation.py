from flask_restful import Resource
from flask import request
from recommenders.cb_recommender import CBRecommender


class MovieRecommendation(Resource):
    @staticmethod
    def get(movie_id):
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        recommendations = CBRecommender.get_recommendations(movie_id, take)
        return recommendations, 200
