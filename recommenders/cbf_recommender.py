from models.svd_recommender import SVDRecommender


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id, k=10):
        recommender = SVDRecommender()
        num_of_rated_items, recommendations = recommender.recommend(user_id, k)
        recommendations = {
            'userId': user_id,
            'ratedItemsCount': num_of_rated_items,
            'recommendations': recommendations
        }

        return recommendations

    @staticmethod
    def get_recommendations_by_genre(user_id, genre_id, k=10):
        recommender = SVDRecommender()
        num_of_rated_items, recommendations = recommender.recommend_by_genre(user_id, genre_id, k)
        recommendations = {
            'userId': user_id,
            'genreId': genre_id,
            'ratedItemsCount': num_of_rated_items,
            'recommendations': recommendations
        }

        return recommendations
