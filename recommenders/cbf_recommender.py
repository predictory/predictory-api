from models.svd_recommender import SVDRecommender
from es.expert_system import ExpertSystem
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

        recommendations = RecommendationsHelper.get_recommendations(ratings, take * 2, skip, user_id, genres)
        recommendations = ExpertSystem.get_scores(user_id, recommendations)

        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations[:take]
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
        recommendations = RecommendationsHelper.get_recommendations(ratings, take * 2, skip, user_id, genres)
        recommendations = ExpertSystem.get_scores(user_id, recommendations)

        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations[:take]
        }

        return recommendations

    @staticmethod
    def get_ratings_for_specific_movies(user_id, movies):
        user_row = RecommendationsHelper.get_user_row(user_id)

        if user_row is not None and len(user_row) > 0:
            user_row = dict((k, user_row[str(k)]) for k in movies if str(k) in user_row)
            user_similarities = RecommendationsHelper.get_similarity_values(user_id, user_row)
        else:
            user_row = dict((k, 0) for k in movies)
            user_similarities = dict((k, 0) for k in movies)
        stats = RecommendationsHelper.get_stats(user_row.keys())
        user_row = RecommendationsHelper.get_pairs(user_row, user_similarities, stats)
        user_row = ExpertSystem.get_scores(user_id, user_row)

        return user_row
