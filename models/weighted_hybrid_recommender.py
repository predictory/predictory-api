from recommenders.cb_recommender import CBRecommender
from recommenders.cbf_recommender import CBFRecommender
from utils.recommendations_helper import RecommendationsHelper


class WeightedHybridRecommender:
    def __init__(self):
        self.MIN_NUM_OF_ITEMS = 10
        self.MAIN_RECOMMENDER_WEIGHT = .8
        self.SECOND_RECOMMENDER_WEIGHT = .2

    def get_recommendations(self, user_id, movie_id, take, skip, genres, movie_type, rec_type, sim_type, sim_source):
        count = len(RecommendationsHelper.get_user_rated_movies(user_id))
        recommendations = []

        if count == 0:
            cb_recommendations = CBRecommender.get_recommendations(movie_id, take, sim_source)
            recommendations.extend(cb_recommendations['recommendations'])
        elif count >= self.MIN_NUM_OF_ITEMS:
            cbf_take = round(take * self.MAIN_RECOMMENDER_WEIGHT)
            cb_take = round(take * self.SECOND_RECOMMENDER_WEIGHT)

            cb_recommendations = CBRecommender.get_recommendations(
                movie_id, cb_take, sim_source)

            if rec_type == 'item-based':
                cbf_recommendations = CBFRecommender.get_recommendations_item_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source)
            elif rec_type == 'user-based':
                cbf_recommendations = CBFRecommender.get_recommendations_user_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source)
            else:
                cbf_recommendations = CBFRecommender.get_recommendations(user_id, cbf_take, skip, genres, movie_type,
                                                                         sim_source)

            recommendations.extend(cbf_recommendations['recommendations'])
            recommendations.extend(cb_recommendations['recommendations'])
        else:
            cbf_take = round(take * self.SECOND_RECOMMENDER_WEIGHT)
            cb_take = round(take * self.MAIN_RECOMMENDER_WEIGHT)

            cb_recommendations = CBRecommender.get_recommendations(
                movie_id, cb_take, sim_source)

            if rec_type == 'item-based':
                cbf_recommendations = CBFRecommender.get_recommendations_item_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source)
            elif rec_type == 'user-based':
                cbf_recommendations = CBFRecommender.get_recommendations_user_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source)
            else:
                cbf_recommendations = CBFRecommender.get_recommendations(user_id, cbf_take, skip, genres, movie_type,
                                                                         sim_source)

            recommendations.extend(cbf_recommendations['recommendations'])
            recommendations.extend(cb_recommendations['recommendations'])

        return recommendations
