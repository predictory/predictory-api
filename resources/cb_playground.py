from flask_restful import Resource
from flask import request
from recommenders.cb_recommender import CBRecommender


class CBPlayground(Resource):

    @staticmethod
    def get(movie_id):
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        rec_type = request.args.get('type', 'tf-idf')
        order_by = request.args.get('order_by', 'similarity,es_score')
        order_by = order_by.split(',')

        recommendations = CBRecommender.get_recommendations(movie_id, take, rec_type, order_by=order_by)
        return recommendations, 200
