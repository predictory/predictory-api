from flask_restful import Resource
from flask import request
from recommenders.cbf_recommender import CBFRecommender


class Search(Resource):
    @staticmethod
    def get(user_id):
        genres = request.args.get('genres')
        movie_type = request.args.get('type')
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)
        include_rated = request.args.get('includeRated')
        include_rated = True if include_rated == 'true' else False
        order_by = request.args.get('order_by', 'rating,es_score')
        order_by = order_by.split(',')
        fav_genres = request.args.get('fav_genres')
        not_fav_genres = request.args.get('not_fav_genres')

        recommendations = CBFRecommender.get_recommendations_for_search(user_id,
                                                                        take,
                                                                        skip,
                                                                        genres,
                                                                        movie_type,
                                                                        include_rated,
                                                                        order_by,
                                                                        fav_genres,
                                                                        not_fav_genres)
        return recommendations, 200

    @staticmethod
    def post(user_id):
        data = request.get_json(force=True)
        order_by = request.args.get('order_by', 'rating,es_score')
        order_by = order_by.split(',')
        fav_genres = request.args.get('fav_genres')
        not_fav_genres = request.args.get('not_fav_genres')
        if 'movies' in data and len(data['movies']) > 0:
            ratings = CBFRecommender.get_ratings_for_specific_movies(user_id, data['movies'], order_by, fav_genres, not_fav_genres)
            response = {
                'userId': user_id,
                'ratings': ratings
            }

            return response, 200
        else:
            return {'message': 'No IDs provided.'}, 400
