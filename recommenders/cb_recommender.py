from models.lda_recommender import LDARecommender
from models.tfidf_recommender import TFIDFRecommender


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
        recommendations = {
            'movieId': movie_id,
            'recommendations': recommender.recommend(movie_id, k)
        }

        return recommendations
