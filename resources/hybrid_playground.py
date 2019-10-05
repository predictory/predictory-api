from flask_restful import Resource
from flask import request
from recommenders.hybrid_recommender import HybridRecommender


class HybridPlayground(Resource):
    @staticmethod
    def get(user_id, movie_id):
        genres = request.args.get('genres')
        movie_type = request.args.get('type')
        rec_type = request.args.get('rec_type', 'svd')
        sim_type = request.args.get('sim_type', 'cosine')
        sim_source = request.args.get('sim_source', 'tf-idf')
        hybrid_type = request.args.get('hybrid_type', 'weighted')
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        order_by = request.args.get('order_by', 'rating,similarity,es_score')
        order_by = order_by.split(',')

        recommendations = HybridRecommender.get_recommendations(user_id, movie_id, hybrid_type, take, skip, genres,
                                                                movie_type, rec_type, sim_type, sim_source, order_by)
        return recommendations, 200
