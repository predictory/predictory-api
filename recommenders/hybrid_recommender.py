from models.weighted_hybrid_recommender import WeightedHybridRecommender


class HybridRecommender:
    @staticmethod
    def get_recommendations(user_id, movie_id, hybrid_type='weighted', take=10, skip=0, genres=None, movie_type=None,
                            rec_type='svd', sim_type='cosine', sim_source='tf-idf'):
        if hybrid_type == 'combined':
            # TODO: create combined recommender
            recommendations = None
        else:
            recommendations = HybridRecommender.get_weighted_recommendations(user_id, movie_id, take, skip, genres,
                                                                             movie_type, rec_type, sim_type, sim_source)

        recommendations = {
            'userId': user_id,
            'movieId': movie_id,
            'recommendations': recommendations
        }

        return recommendations

    @staticmethod
    def get_weighted_recommendations(user_id, movie_id, take, skip, genres, movie_type, rec_type, sim_type, sim_source):
        recommender = WeightedHybridRecommender()
        recommendations = recommender.get_recommendations(user_id, movie_id, take, skip, genres, movie_type, rec_type,
                                                          sim_type, sim_source)

        return recommendations
