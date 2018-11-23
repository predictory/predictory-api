from flask_restful import fields, marshal
from models.movie import MovieModel
from db import db
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import nltk
from sklearn.neighbors import NearestNeighbors

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                     min_df=0, stop_words='english')
nltk.download('wordnet', quiet=True)
np.random.seed(2018)
stemmer = PorterStemmer()

movies_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'plot': fields.String
}

class CBRecommender():
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
    def lda(movie_id, n = 10):
        metric = 'cosine'

        movies = MovieModel.query.all()
        data = pd.DataFrame(marshal(movies, movies_fields))

        documents = data['plot']
        ids = data['id']

        processed_docs = documents.map(CBRecommender.preprocess)

        dictionary = gensim.corpora.Dictionary(processed_docs)
        dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
        corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        
        lda = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=30, id2word=dictionary, passes=2, minimum_probability=0.0)
        docs_topics = np.array([[tup[1] for tup in lst] for lst in lda[corpus_tfidf]])
        df_docs_topics = pd.DataFrame(docs_topics, index=data.index)

        similarities=[]
        indices=[]
        model_knn = NearestNeighbors(metric = metric, algorithm = 'brute') 
        model_knn.fit(df_docs_topics)

        distances, indices = model_knn.kneighbors(df_docs_topics.iloc[movie_id, :].values.reshape(1, -1), n_neighbors = n + 1)
        similarities = 1 - distances.flatten()
        similarities = similarities[1:]
        indices = indices.flatten()
        indices = indices[1:]
        ids = ids[indices].values
        recommendations = {
            'movieId': movie_id,
            'recommendations': [{str(indices[index]): float(line)} for index, line in enumerate(similarities)]
        }

        return recommendations

    @staticmethod
    def lemmatize_stemming(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
    
    @staticmethod
    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(CBRecommender.lemmatize_stemming(token))
        return result

