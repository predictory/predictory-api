from recommenders.cb_recommender import CBRecommender
from recommenders.cbf_recommender import CBFRecommender
from models.user_rating import UserRatingModel


class WeightedHybridRecommender:
    def __init__(self):
        self.MIN_NUM_OF_ITEMS = 10
        self.MAIN_RECOMMENDER_WEIGHT = .8
        self.SECOND_RECOMMENDER_WEIGHT = .2

    def get_recommendations(self, user_id, movie_id, k=10):
        cb_recommender = CBRecommender()
        cbf_recommender = CBFRecommender()
        count = len(UserRatingModel.query.filter_by(userId=user_id).all())
        recommendations = []

        if count == 0:
            cb_recommendations = cb_recommender.get_recommendations(movie_id, k)
            recommendations.extend(cb_recommendations['recommendations'])
        elif count >= self.MIN_NUM_OF_ITEMS:
            cbf_recommendations = cbf_recommender.get_recommendations(
                user_id,
                round(k * self.MAIN_RECOMMENDER_WEIGHT))
            cb_recommendations = cb_recommender.get_recommendations(
                movie_id,
                round(k * self.SECOND_RECOMMENDER_WEIGHT))
            recommendations.extend(cbf_recommendations['recommendations'])
            recommendations.extend(cb_recommendations['recommendations'])
        else:
            cbf_recommendations = cbf_recommender.get_recommendations(
                user_id,
                round(k * self.SECOND_RECOMMENDER_WEIGHT))
            cb_recommendations = cb_recommender.get_recommendations(
                movie_id,
                round(k * self.MAIN_RECOMMENDER_WEIGHT))
            recommendations.extend(cbf_recommendations['recommendations'])
            recommendations.extend(cb_recommendations['recommendations'])

        return recommendations
