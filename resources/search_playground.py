from flask_restful import Resource
from flask import request
from es.expert_system import ExpertSystem
from utils.recommendations_helper import RecommendationsHelper


class SearchPlayground(Resource):

    @staticmethod
    def post(user_id):
        data = request.get_json(force=True)
        rec_type = request.args.get('rec_type', 'svd')
        sim_type = request.args.get('sim_type', 'cosine')
        sim_source = request.args.get('sim_source', 'cosine')

        if 'movies' in data and len(data['movies']) > 0:
            if rec_type == 'item-based':
                rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)
                user_row = RecommendationsHelper.get_user_movies_custom_based(rated_movies, user_id, rec_type=rec_type,
                                                                              sim_type=sim_type)
            elif rec_type == 'user-based':
                rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)
                user_row = RecommendationsHelper.get_user_movies_custom_based(rated_movies, user_id, rec_type=rec_type,
                                                                              sim_type=sim_type)
            else:
                user_row = RecommendationsHelper.get_user_row(user_id)

            if user_row is not None and len(user_row) > 0:
                if rec_type == 'item-based' or rec_type == 'user-based':
                    user_row = dict((k, user_row[k]) for k in data['movies'] if k in user_row)
                else:
                    user_row = dict((k, user_row[str(k)]) for k in data['movies'] if str(k) in user_row)
                user_similarities = RecommendationsHelper.get_similarity_values(user_id, user_row,
                                                                                sim_source=sim_source)
            else:
                user_row = dict((k, 0) for k in data['movies'])
                user_similarities = dict((k, 0) for k in data['movies'])
            stats = RecommendationsHelper.get_stats(user_row.keys())
            user_row = RecommendationsHelper.get_pairs(user_row, user_similarities, stats)
            user_row = ExpertSystem.get_scores(user_id, user_row)

            response = {
                'userId': user_id,
                'ratings': user_row
            }

            return response, 200
        else:
            return {'message': 'No IDs provided.'}, 400
