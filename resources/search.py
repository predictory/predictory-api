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
