from models.lda_recommender import LDARecommender
from models.tfidf_recommender import TFIDFRecommender
from utils.recommendations_helper import RecommendationsHelper


class CBRecommender:
    @staticmethod
    def get_recommendations(movie_id, k=10):
        recommendations = CBRecommender.tf_idf(movie_id, k)
        return recommendations

    @staticmethod
    def lda(movie_id, k=10):
        recommender = LDARecommender()
        recommendations = {
            'movieId': movie_id,
            'recommendations': recommender.recommend(movie_id, k)
        }
        return recommendations

    @staticmethod
    def tf_idf(movie_id, k=10):
        recommender = TFIDFRecommender()
        recommendations = recommender.recommend(movie_id, k)
        keys = [row['id'] for row in recommendations]
        stats = RecommendationsHelper.get_stats(keys)
        recommendations = [{
            'id': row['id'],
            'similarity': row['similarity'],
            'average_rating': stats[row['id']]['average_rating'],
            'ratings_count': stats[row['id']]['count'],
            'penalized': stats[row['id']]['penalized']
        } for row in recommendations]

        recommendations = {
            'movieId': movie_id,
            'recommendations': recommendations
        }

        return recommendations
