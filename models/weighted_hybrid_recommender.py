from recommenders.cb_recommender import CBRecommender
from recommenders.cbf_recommender import CBFRecommender


class WeightedHybridRecommender:
    def __init__(self):
        self.MIN_NUM_OF_ITEMS = 10
        self.MAIN_RECOMMENDER_WEIGHT = .8
        self.SECOND_RECOMMENDER_WEIGHT = .2
        self.NUM_OF_RECOMMENDATIONS = 10

    def get_recommendations(self, user_id, movie_id):
        cb_recommender = CBRecommender()
        cbf_recommender = CBFRecommender()

        return None
