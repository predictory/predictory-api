from recommenders.cb_recommender import CBRecommender
from recommenders.cbf_recommender import CBFRecommender
from utils.recommendations_helper import RecommendationsHelper


class WeightedHybridRecommender:
    def __init__(self):
        self.MIN_NUM_OF_ITEMS = 20
        self.MAIN_RECOMMENDER_WEIGHT = .8
        self.SECOND_RECOMMENDER_WEIGHT = .2

    def get_recommendations(self, user_id, movie_id, take, skip, genres, movie_type, rec_type, sim_type, sim_source,
                            order_by):
        count = len(RecommendationsHelper.get_user_rated_movies(user_id))
        recommendations = []
        cb_order_columns = ['similarity', 'es_score']
        cbf_order_columns = ['rating', 'es_score']
        cb_order_by = [column for column in order_by if column in cb_order_columns]
        cbf_order_by = [column for column in order_by if column in cbf_order_columns]

        if count == 0:
            cb_recommendations = CBRecommender.get_recommendations(movie_id, take, sim_source, genres, movie_type,
                                                                   cb_order_by)
            recommendations.extend(cb_recommendations['recommendations'])
        elif count >= self.MIN_NUM_OF_ITEMS:
            cbf_take = round(take * self.MAIN_RECOMMENDER_WEIGHT)
            cb_take = round(take * self.SECOND_RECOMMENDER_WEIGHT)

            cb_recommendations = CBRecommender.get_recommendations(movie_id, cb_take, sim_source, genres, movie_type,
                                                                   cb_order_by)
            if rec_type == 'item-based':
                cbf_recommendations = CBFRecommender.get_recommendations_item_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source,
                                                                                    cbf_order_by)
            elif rec_type == 'user-based':
                cbf_recommendations = CBFRecommender.get_recommendations_user_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source,
                                                                                    cbf_order_by)
            else:
                cbf_recommendations = CBFRecommender.get_recommendations(user_id, cbf_take, skip, genres, movie_type,
                                                                         sim_source, cbf_order_by)

            recommendations.extend(cbf_recommendations['recommendations'])
            recommendations.extend(cb_recommendations['recommendations'])
        else:
            cbf_take = round(take * self.SECOND_RECOMMENDER_WEIGHT)
            cb_take = round(take * self.MAIN_RECOMMENDER_WEIGHT)

            cb_recommendations = CBRecommender.get_recommendations(movie_id, cb_take, sim_source, genres, movie_type,
                                                                   cb_order_by)
            if rec_type == 'item-based':
                cbf_recommendations = CBFRecommender.get_recommendations_item_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source,
                                                                                    cbf_order_by)
            elif rec_type == 'user-based':
                cbf_recommendations = CBFRecommender.get_recommendations_user_based(user_id, cbf_take, skip, genres,
                                                                                    movie_type, sim_type, sim_source,
                                                                                    cbf_order_by)
            else:
                cbf_recommendations = CBFRecommender.get_recommendations(user_id, cbf_take, skip, genres, movie_type,
                                                                         sim_source, cbf_order_by)

            recommendations.extend(cbf_recommendations['recommendations'])
            recommendations.extend(cb_recommendations['recommendations'])

        return recommendations
