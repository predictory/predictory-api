from models.svd_recommender import SVDRecommender
from models.item_based_recommender import ItemBasedRecommender
from models.user_based_recommender import UserBasedRecommender
from es.expert_system import ExpertSystem
from utils.recommendations_helper import RecommendationsHelper
from utils.data_helper import DataHelper


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id, take=10, skip=0, genres=None, movie_type=None, sim_source='tf-idf',
                            order_by=['rating', 'es_score'], fav_genres=None, not_fav_genres=None):
        recommender = SVDRecommender()

        if genres is not None:
            genres_ids = genres.split(',')
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id, genres_ids,
                                                                                         movie_type)
        else:
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend(user_id)

        ratings, num_of_ratings = RecommendationsHelper.process_genres(ratings, fav_genres, not_fav_genres)

        recommendations = DataHelper.prepare_cbf_data(user_id, num_of_rated_items, ratings, take, skip, genres,
                                                      sim_source, order_by)
        recommendations = DataHelper.pack_recommendations_for_response(user_id, recommendations, num_of_rated_items,
                                                                       num_of_ratings)

        return recommendations

    @staticmethod
    def get_recommendations_for_search(user_id, take, skip, genres, movie_type=None, include_rated=False,
                                       order_by=['rating', 'es_score'], fav_genres=None, not_fav_genres=None):
        recommender = SVDRecommender()

        genres_ids = genres.split(',')
        num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id,
                                                                                     genres_ids,
                                                                                     movie_type,
                                                                                     include_rated)
        ratings, num_of_ratings = RecommendationsHelper.process_genres(ratings, fav_genres, not_fav_genres)

        recommendations = DataHelper.prepare_cbf_data(user_id, num_of_rated_items, ratings, take, skip, genres,
                                                      order_by=order_by)
        recommendations = DataHelper.pack_recommendations_for_response(user_id, recommendations, num_of_rated_items,
                                                                       num_of_ratings)

        return recommendations

    @staticmethod
    def get_ratings_for_specific_movies(user_id, movies, order_by=['rating', 'es_score'], fav_genres=None,
                                        not_fav_genres=None):
        user_row = RecommendationsHelper.get_user_row(user_id)

        if user_row is not None and len(user_row) > 0:
            user_row = dict((k, user_row[str(k)]) for k in movies if str(k) in user_row)
            user_similarities = RecommendationsHelper.get_similarity_values(user_id, user_row)
        else:
            user_row = dict((k, 0) for k in movies)
            user_similarities = dict((k, 0) for k in movies)

        user_row = [(key, user_row[key]) for key in user_row]
        user_row, num_of_items = RecommendationsHelper.process_genres(user_row, fav_genres, None)
        user_row = {item[0]: item[1] for item in user_row}

        stats = RecommendationsHelper.get_stats(user_row.keys())
        user_row = RecommendationsHelper.get_pairs(user_row, user_similarities, stats)
        user_row = ExpertSystem.get_scores(user_id, user_row)
        user_row = RecommendationsHelper.compute_augmented_rating(user_row)
        user_row = RecommendationsHelper.sort(user_row, order_by)

        return user_row

    @staticmethod
    def get_recommendations_item_based(user_id, take=10, skip=0, genres=None, movie_type=None, sim_type='cosine',
                                       sim_source='tf-idf', order_by=['rating', 'es_score'], fav_genres=None,
                                       not_fav_genres=None):
        recommender = ItemBasedRecommender()

        if genres is not None:
            genres_ids = genres.split(',')
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id, genres_ids,
                                                                                         movie_type, sim_type=sim_type)
        else:
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend(user_id, sim_type)

        ratings, num_of_ratings = RecommendationsHelper.process_genres(ratings, fav_genres, not_fav_genres)

        recommendations = DataHelper.prepare_cbf_data(user_id, num_of_rated_items, ratings, take, skip, genres,
                                                      sim_source, order_by)
        recommendations = DataHelper.pack_recommendations_for_response(user_id, recommendations, num_of_rated_items,
                                                                       num_of_ratings)

        return recommendations

    @staticmethod
    def get_recommendations_user_based(user_id, take=10, skip=0, genres=None, movie_type=None, sim_type='cosine',
                                       sim_source='tf-idf', order_by=['rating', 'es_score'], fav_genres=None,
                                       not_fav_genres=None):
        recommender = UserBasedRecommender()

        if genres is not None:
            genres_ids = genres.split(',')
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend_by_genre(user_id, genres_ids,
                                                                                         movie_type, sim_type=sim_type)
        else:
            num_of_rated_items, num_of_ratings, ratings = recommender.recommend(user_id, sim_type)

        ratings, num_of_ratings = RecommendationsHelper.process_genres(ratings, fav_genres, not_fav_genres)

        recommendations = DataHelper.prepare_cbf_data(user_id, num_of_rated_items, ratings, take, skip, genres,
                                                      sim_source, order_by)
        recommendations = DataHelper.pack_recommendations_for_response(user_id, recommendations, num_of_rated_items,
                                                                       num_of_ratings)

        return recommendations
