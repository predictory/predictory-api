from flask_restful import Resource
from flask import request
from recommenders.cb_recommender import CBRecommender


class MovieRecommendation(Resource):
    @staticmethod
    def get(movie_id):
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        rec_type = request.args.get('type', 'tf-idf')
        recommendations = CBRecommender.get_recommendations(movie_id, take, rec_type)
        return recommendations, 200
