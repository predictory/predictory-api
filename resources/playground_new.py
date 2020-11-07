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

            # increase rating for fav genres and decrease for not fav genres
            recommendations = RecommendationsHelper.process_genres_increase_decrease_rating(recommendations, fav_genres, not_fav_genres)

            # boost rating for 5 top items from genre

            recommendations = RecommendationsHelper.process_genres_increase_top_movies_rating(recommendations, fav_genres)

            users = users.tolist()
            users.remove(user_id)
            recommendations = RecommendationsHelper.process_genres_increase_for_part_of_group(recommendations, users)

            recommendations = [{'id': k, 'rating': v} for k, v in
                               sorted(recommendations.items(), key=lambda item: item[1], reverse=True)]

            return recommendations[skip:take], 200
        else:
            print(f'[Retrain]: User with id {user_id} has no recommendations')
            return 404
