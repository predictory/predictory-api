from flask_restful import Resource
from flask import request
from recommenders.cbf_recommender import CBFRecommender


class CBFPlayground(Resource):

    @staticmethod
    def get(user_id):
        genres = request.args.get('genres')
        movie_type = request.args.get('type')
        rec_type = request.args.get('rec_type', 'svd')
        sim_type = request.args.get('sim_type', 'cosine')
        sim_source = request.args.get('sim_source', 'tf-idf')
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        order_by = request.args.get('order_by', 'rating,es_score')
        order_by = order_by.split(',')

        if rec_type == 'item-based':
            recommendations = CBFRecommender.get_recommendations_item_based(user_id, take, skip, genres, movie_type,
                                                                            sim_type, sim_source, order_by)
        elif rec_type == 'user-based':
            recommendations = CBFRecommender.get_recommendations_user_based(user_id, take, skip, genres, movie_type,
                                                                            sim_type, sim_source, order_by)
        else:
            recommendations = CBFRecommender.get_recommendations(user_id, take, skip, genres, movie_type, sim_source,
                                                                 order_by)

        return recommendations, 200
