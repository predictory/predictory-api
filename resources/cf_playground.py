from flask_restful import Resource
from flask import request
from recommenders.cbf_recommender import CBFRecommender


class CFPlayground(Resource):

    @staticmethod
    def get(user_id):
        genres = request.args.get('genres')
        movie_type = request.args.get('type')
        rec_type = request.args.get('rec_type', 'svd')
        sim_type = request.args.get('sim_type', 'cosine')
        sim_source = request.args.get('sim_source', 'tf-idf')
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)

        if rec_type == 'item-based':
            recommendations = CBFRecommender.get_recommendations_item_based(user_id, take, skip, genres, movie_type,
                                                                            sim_type, sim_source)
        elif rec_type == 'user-based':
            recommendations = CBFRecommender.get_recommendations_user_based(user_id, take, skip, genres, movie_type,
                                                                            sim_type, sim_source)
        else:
            recommendations = CBFRecommender.get_recommendations(user_id, take, skip, genres, movie_type, sim_source)

        return recommendations, 200
