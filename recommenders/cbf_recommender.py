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

        recommendations = RecommendationsHelper.get_recommendations(ratings, take, skip)

        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations
        }

        return recommendations

    @staticmethod
    def get_recommendations_for_search(user_id, take, skip, genres, movie_type=None):
        recommender = SVDRecommender()

        genres_ids = genres.split(',')
        num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id, genres_ids,
                                                                                     movie_type)
        recommendations = RecommendationsHelper.get_recommendations(ratings, take, skip)

        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations
        }

        return recommendations
