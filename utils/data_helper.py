from es.expert_system import ExpertSystem
from utils.recommendations_helper import RecommendationsHelper


class DataHelper:

    @staticmethod
    def prepare_cbf_data(user_id, num_of_rated_items, ratings, take=10, skip=0, genres=None, sim_source='tf-idf',
                         order_by=['rating', 'es_score']):
        pre_take = take * 3 if order_by == ['rating', 'es_score'] or order_by == ['rating'] else -1
        if ratings is not None and num_of_rated_items > 0:
            recommendations = RecommendationsHelper.get_recommendations(ratings, pre_take, skip, user_id, genres,
                                                                        sim_source)
            recommendations = ExpertSystem.get_scores(user_id, recommendations)
            recommendations = RecommendationsHelper.compute_augmented_rating(recommendations)
            recommendations = RecommendationsHelper.sort(recommendations, order_by)
            recommendations = recommendations[:take]
        else:
            recommendations = ratings

        return recommendations

    @staticmethod
    def pack_recommendations_for_response(user_id, recommendations, num_of_rated_items, num_of_ratings):
        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'ratingsCount': num_of_ratings,
            'recommendations': recommendations
        }

        return recommendations
