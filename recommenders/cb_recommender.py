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
    def tf_idf(movie_id):
        movies = MovieModel.query.all()
        data = pd.DataFrame(marshal(movies, movies_fields))
        tfidf_matrix = tf.fit_transform(data['plot'])
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        ids = data['id']
        indices = pd.Series(data.index, index=data['id'])

        idx = indices[movie_id]
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:int(10) + 1]
        recommendations = {
            'movieId': movie_id,
            'recommendations': [{i[0]: i[1]} for i in sim_scores]
        }

        return recommendations

    @staticmethod
    def lda(movie_id):
        recommender = LDARecommender()
        result = recommender.recommend(movie_id)
        return result
