from flask_restful import fields, marshal
from models.movie import MovieModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.lda_recommender import LDARecommender

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                     min_df=0, stop_words='english')

movies_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'plot': fields.String
}


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
