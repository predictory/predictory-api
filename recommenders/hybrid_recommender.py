from models.weighted_hybrid_recommender import WeightedHybridRecommender
from models.switched_hybrid_recommender import SwitchedHybridRecommender


class HybridRecommender:
    @staticmethod
    def get_recommendations(user_id, movie_id, hybrid_type='weighted', take=10, skip=0, genres=None, movie_type=None,
                            rec_type='svd', sim_type='cosine', sim_source='tf-idf',
                            order_by=['rating', 'similarity', 'es_score']):
        if hybrid_type == 'switched':
            recommendations = HybridRecommender.get_switched_recommendations(user_id, movie_id, take, skip, genres,
                                                                             movie_type, rec_type, sim_type, sim_source,
                                                                             order_by)
        else:
            recommendations = HybridRecommender.get_weighted_recommendations(user_id, movie_id, take, skip, genres,
                                                                             movie_type, rec_type, sim_type, sim_source,
                                                                             order_by)

        recommendations = {
            'userId': user_id,
            'movieId': movie_id,
            'recommendations': recommendations
        }

        return recommendations

    @staticmethod
    def get_weighted_recommendations(user_id, movie_id, take, skip, genres, movie_type, rec_type, sim_type, sim_source,
                                     order_by):
        recommender = WeightedHybridRecommender()
        recommendations = recommender.get_recommendations(user_id, movie_id, take, skip, genres, movie_type, rec_type,
                                                          sim_type, sim_source, order_by)

        return recommendations

    @staticmethod
    def get_switched_recommendations(user_id, movie_id, take, skip, genres, movie_type, rec_type, sim_type, sim_source,
                                     order_by):
        recommender = SwitchedHybridRecommender()
        recommendations = recommender.get_recommendations(user_id, movie_id, take, skip, genres, movie_type, rec_type,
                                                          sim_type, sim_source, order_by)

        return recommendations
