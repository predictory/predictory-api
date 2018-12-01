from models.lda_recommender import LDARecommender
from models.tfidf_recommender import TFIDFRecommender


class CBRecommender:
    @staticmethod
    def get_recommendations(movie_id):
        recommendations = CBRecommender.lda(movie_id)
        return recommendations

    @staticmethod
    def lda(movie_id):
        recommender = LDARecommender()
        recommendations = {
            'movieId': movie_id,
            'recommendations': recommender.recommend(movie_id)
        }
        return recommendations

    @staticmethod
    def tf_idf(movie_id):
        recommender = TFIDFRecommender()
        recommendations = {
            'movieId': movie_id,
            'recommendations': recommender.recommend(movie_id)
        }

        return recommendations
