from models.svd_recommender import SVDRecommender


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id, k=10):
        recommendations = CBFRecommender.svd(user_id, k)
        return recommendations

    @staticmethod
    def svd(user, k=10):
        recommender = SVDRecommender()
        num_of_rated_items, recommendations = recommender.recommend(user, k)
        result = {
            'userId': user,
            'ratedItemsCount': num_of_rated_items,
            'recommendations': recommendations
        }

        return result
