from utils.recommendations_helper import RecommendationsHelper
from recommenders.cbf_recommender import CBFRecommender
from recommenders.cb_recommender import CBRecommender


class SwitchedHybridRecommender:
    def __init__(self):
        self.MIN_NUM_OF_ITEMS = 20

    def get_recommendations(self, user_id, movie_id, take, skip, genres, movie_type, rec_type, sim_type, sim_source,
                            order_by):
        count = len(RecommendationsHelper.get_user_rated_movies(user_id))
        recommendations = []

        if count >= self.MIN_NUM_OF_ITEMS:
            if rec_type == 'item-based':
                cbf_recommendations = CBFRecommender.get_recommendations_item_based(user_id, take, skip, genres,
                                                                                    movie_type, sim_type, sim_source,
                                                                                    order_by)
            elif rec_type == 'user-based':
                cbf_recommendations = CBFRecommender.get_recommendations_user_based(user_id, take, skip, genres,
                                                                                    movie_type, sim_type, sim_source,
                                                                                    order_by)
            else:
                cbf_recommendations = CBFRecommender.get_recommendations(user_id, take, skip, genres, movie_type,
                                                                         sim_source, order_by)

            recommendations.extend(cbf_recommendations['recommendations'])
        else:
            cb_recommendations = CBRecommender.get_recommendations(movie_id, take, sim_source, genres, movie_type,
                                                                   order_by)
            recommendations.extend(cb_recommendations['recommendations'])

        return recommendations
