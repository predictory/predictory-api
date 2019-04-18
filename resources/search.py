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

        recommendations = CBFRecommender.get_recommendations_for_search(user_id, take, skip, genres, movie_type)
        return recommendations, 200

    @staticmethod
    def post(user_id):
        data = request.get_json(force=True)
        if 'movies' in data and len(data['movies']) > 0:
            ratings = CBFRecommender.get_ratings_for_specific_movies(user_id, data['movies'])
            response = {
                'userId': user_id,
                'ratings': ratings
            }

            return response, 200
        else:
            return {'message': 'No IDs provided.'}, 400
