from models.svd_recommender import SVDRecommender


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id):
        recommendations = CBFRecommender.svd(user_id, 10)
        return recommendations

    @staticmethod
    def svd(user, n):
        recommender = SVDRecommender()
        recommendations = {
            'userId': user,
            'recommendations': recommender.recommend(user, n)
        }

        return recommendations
