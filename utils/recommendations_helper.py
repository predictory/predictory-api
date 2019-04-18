import pandas as pd
from mongo import mongo


class RecommendationsHelper:

    @staticmethod
    def get_dict(ratings, take=10, skip=0):
        return dict(ratings[skip:skip + take])

    @staticmethod
    def get_id_rating_pairs(ratings):
        return [{'id': key, 'rating': float(value)} for key, value in ratings.items()]

    @staticmethod
    def get_user_row(user_id):
        mongo_ratings = mongo.db.users_ratings

        user_row = mongo_ratings.find_one({'id': user_id})
        return user_row['ratings']

    @staticmethod
    def get_user_movies(rated_movies, user_id):
        user_rated_movies = list(map(str, pd.DataFrame(rated_movies)['movieId'].values))
        user_row = RecommendationsHelper.get_user_row(user_id)

        for movie in user_rated_movies:
            try:
                del user_row[movie]
            except:
                print('Movie not found')

        return user_row

    @staticmethod
    def get_recommendations(ratings, take, skip):
        recommended_movies = RecommendationsHelper.get_dict(ratings, take, skip)
        return RecommendationsHelper.get_id_rating_pairs(recommended_movies)
