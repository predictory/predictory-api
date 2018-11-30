from models.svd_recommender import SVDRecommender


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id):
        recommendations = CBFRecommender.svd(user_id, 10)
        return recommendations

    @staticmethod
    def svd(user, n):
        recommender = SVDRecommender()
        num_of_rated_items, recommendations = recommender.recommend(user, n)
        result = {
            'userId': user,
            'ratedItemsCount': num_of_rated_items,
            'recommendations': recommendations
        }

        return result
