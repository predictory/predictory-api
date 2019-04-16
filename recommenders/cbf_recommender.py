from models.svd_recommender import SVDRecommender


class CBFRecommender:
    @staticmethod
    def get_recommendations(user_id, take=10, skip=0, genres=None, movie_type=None):
        recommender = SVDRecommender()
        recommendations = {
            'userId': user_id,
            'ratedItemsCount': 0,
            'recommendations': None
        }

        if genres is not None:
            genres_ids = genres.split(',')
            num_of_rated_items, recommendations = recommender.recommend_by_genre(user_id, genres_ids, movie_type, take, skip)

            recommendations = {
                'userId': user_id,
                'genresIds': genres_ids,
                'ratedItemsCount': num_of_rated_items,
                'recommendations': recommendations
            }
        else:
            num_of_rated_items, recommendations = recommender.recommend(user_id, take, skip)

            recommendations = {
                'userId': user_id,
                'ratedItemsCount': num_of_rated_items,
                'recommendations': recommendations
            }

        return recommendations
