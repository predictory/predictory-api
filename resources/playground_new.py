from flask_restful import Resource
from models.svd_model import SVDModel
from utils.database_helper import DatabaseHelper
import pandas as pd
from flask import request
from utils.recommendations_helper import RecommendationsHelper


class PlaygroundNew(Resource):
    @staticmethod
    def get(user_id):
        svd_model = SVDModel()
        data, movies, users, fav_genres, not_fav_genres = DatabaseHelper.load_data_matrix_limited_by_top_genres(user_id)
        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)
        U, sigma, Vt, predicted_ratings = svd_model.train(data, 20)
        ratings_df = pd.DataFrame(predicted_ratings, columns=movies, index=users)
        take = request.args.get('take', 10, int)
        skip = request.args.get('skip', 0, int)

        if user_id in ratings_df.index:
            recommendations = ratings_df.loc[user_id].to_dict()
            for movie in rated_movies:
                try:
                    del recommendations[movie['movieId']]
                except:
                    print('Movie not found')
            recommendations = [{'id': k, 'rating': v} for k, v in sorted(recommendations.items(), key=lambda item: item[1], reverse=True)]

            # boost rating for items from favourite genres
            # boost rating for 5 top items from genre
            # reduce rating for items from not favourites genres

            return recommendations[skip:take], 200
        else:
            print(f'[Retrain]: User with id {user_id} has no recommendations')
            return 404
