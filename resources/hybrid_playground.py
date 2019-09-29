from flask_restful import Resource
from flask import request
from recommenders.hybrid_recommender import HybridRecommender


class HybridPlayground(Resource):
    @staticmethod
    def get(user_id, movie_id):
        rec_type = request.args.get('rec_type', 'svd')
        sim_type = request.args.get('sim_type', 'cosine')
        sim_source = request.args.get('sim_source', 'tf-idf')
        hybrid_type = request.args.get('hybrid_type', 'weighted')
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)

        recommendations = HybridRecommender.get_recommendations(user_id, movie_id, hybrid_type, take, skip,
                                                                rec_type=rec_type, sim_type=sim_type,
                                                                sim_source=sim_source)
        return recommendations, 200
