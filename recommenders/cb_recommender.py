from models.lda_recommender import LDARecommender
from models.tfidf_recommender import TFIDFRecommender
from utils.recommendations_helper import RecommendationsHelper
from es.expert_system import ExpertSystem


class CBRecommender:
    @staticmethod
    def get_recommendations(movie_id, k=10, rec_type='tf-idf', genres=None, movie_type=None,
                            order_by=['similarity', 'es_score']):
        print(f"Recommending for: {rec_type}, movie ID: {movie_id}, K: {k}")
        if rec_type == 'lda':
            recommendations = LDARecommender.recommend(movie_id, k, genres, movie_type)
        else:
            recommendations = TFIDFRecommender.recommend(movie_id, k, genres, movie_type)

        keys = [row['id'] for row in recommendations]
        stats = RecommendationsHelper.get_stats(keys)
        recommendations = [{
            'id': row['id'],
            'similarity': row['similarity'],
            'average_rating': stats[int(row['id'])]['average_rating'],
            'ratings_count': stats[int(row['id'])]['count'],
            'penalized': stats[int(row['id'])]['penalized']
        } for row in recommendations]
        recommendations = ExpertSystem.get_scores(movie_id, recommendations)
        recommendations = RecommendationsHelper.sort(recommendations, order_by)

        recommendations = {
            'movieId': movie_id,
            'recommendations': recommendations[:k]
        }

        return recommendations
