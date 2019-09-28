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
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)

        if rec_type == 'item-based':
            # TODO: create item-based recommender
            recommendations = CBFRecommender.get_recommendations_item_based(user_id, take, skip, genres, movie_type,
                                                                            sim_type)
        elif rec_type == 'user-based':
            # TODO: create user-based recommender
            recommendations = {'dummy': 'content'}
        else:
            recommendations = CBFRecommender.get_recommendations(user_id, take, skip, genres, movie_type)

        return recommendations, 200
