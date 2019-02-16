from models.weighted_hybrid_recommender import WeightedHybridRecommender


class HybridRecommender:
    @staticmethod
    def get_recommendations(user_id, movie_id):
        recommendations = {
            'userId': user_id,
            'movieId': movie_id,
            'recommendations': HybridRecommender.get_weighted_recommendations(user_id, movie_id)
        }

        return recommendations

    @staticmethod
    def get_weighted_recommendations(user_id, movie_id):
        recommender = WeightedHybridRecommender()
        recommendations = recommender.get_recommendations(user_id, movie_id)

        return recommendations
