from models.svd_recommender import SVDRecommender
from utils.recommendations_helper import RecommendationsHelper


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id, take=10, skip=0, genres=None, movie_type=None):
        recommender = SVDRecommender()

        if genres is not None:
            genres_ids = genres.split(',')
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id, genres_ids,
                                                                                         movie_type)
        else:
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend(user_id)

        recommendations = RecommendationsHelper.get_recommendations(ratings, take, skip, user_id, genres)

        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations
        }

        return recommendations

    @staticmethod
    def get_recommendations_for_search(user_id, take, skip, genres, movie_type=None, include_rated=False):
        recommender = SVDRecommender()

        genres_ids = genres.split(',')
        num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id,
                                                                                     genres_ids,
                                                                                     movie_type,
                                                                                     include_rated)
        recommendations = RecommendationsHelper.get_recommendations(ratings, take, skip, user_id, genres)

        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations
        }

        return recommendations

    @staticmethod
    def get_ratings_for_specific_movies(user_id, movies):
        user_row = RecommendationsHelper.get_user_row(user_id)
        user_row = dict((k, user_row[str(k)]) for k in movies if str(k) in user_row)
        if len(user_row) > 0:
            user_row = [{'id': k, 'rating': user_row[k]} for k in user_row]

        return user_row
