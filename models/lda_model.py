import os
from flask_restful import fields, marshal
import nltk
import itertools
import numpy as np
import pandas as pd
from nltk.stem.porter import *
import pickle
from nltk.stem import WordNetLemmatizer
from scipy.sparse import coo_matrix
from models.movie import MovieModel
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import models, parsing
from gensim.models import LdaModel
from utils.pandas_helper import PandasHelper
from sklearn.neighbors import NearestNeighbors


nltk.download('wordnet', quiet=True)
np.random.seed(2018)
stemmer = PorterStemmer()

movies_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'plot': fields.String
}


class LDAModel:
    def __init__(self):
        self.no_below = 5
        self.no_above = 0.2
        self.num_topics = 10
        self.num_of_iterations = 100
        self.passes = 3
        self.minimum_probability = 0.01
        self.num_similarities = 30

    @staticmethod
    def lemmatize_stemming(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text))

    @staticmethod
    def preprocess(text):
        unigrams = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in parsing.preprocessing.STOPWORDS and len(token) > 3:
                unigrams.append(LDAModel.lemmatize_stemming(token))

        return list(itertools.chain(unigrams))

    @staticmethod
    def save_pickle_file(file_name, data):
        file_name = f'./models/LDA/{file_name}.pickle'
        mapping_file = open(file_name, 'wb')
        pickle.dump(data, mapping_file)
        mapping_file.close()

    @staticmethod
    def save_model(lda, similarities):
        if not os.path.exists('./models/LDA'):
            os.makedirs('./models/LDA')
        # Save model output
        lda.save('./models/LDA/model')
        LDAModel.save_pickle_file('similarities', similarities)

    def get_similarities(self, index, ids):
        sims = []
        coo = coo_matrix(index)
        similarity_matrix = np.zeros(((len(ids)), len(ids)))

        print('Started getting LDA similarities')
        for i, j, v in zip(coo.row, coo.col, coo.data):
            similarity_matrix[i, j] = 1 if v > 1 else v

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(similarity_matrix)

        df_similarity_matrix = pd.DataFrame(similarity_matrix, index=ids)
        for i, row in df_similarity_matrix.iterrows():
            movie_row = row.values.reshape(1, -1)

            distances, indices = model_knn.kneighbors(movie_row, n_neighbors=self.num_similarities + 1)
            similarities = 1 - distances.flatten()
            similarities = similarities[1:]
            indices = indices.flatten()
            indices = indices[1:]

            sims.append({
                'id': i,
                'similarities': [{
                    'id': PandasHelper.get_id_from_series(df_similarity_matrix.iloc[[indices[index]]]),
                    'similarity': float(line)
                } for index, line in enumerate(similarities)]
            })
        print('Finished getting LDA similarities')

        return sims

    def train_model(self):
        movies = MovieModel.query.all()
        data = pd.DataFrame(marshal(movies, movies_fields))

        documents = data['plot']
        ids = data['id']
        processed_docs = documents.map(LDAModel.preprocess)

        print('Start training LDA model...')
        dictionary = gensim.corpora.Dictionary(processed_docs)
        dictionary.filter_extremes(no_below=self.no_below, no_above=self.no_above)
        corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

        tf_idf = models.TfidfModel(corpus)
        corpus_tf_idf = tf_idf[corpus]

        lda = LdaModel(
            corpus_tf_idf,
            num_topics=self.num_topics,
            id2word=dictionary,
            passes=self.passes,
            iterations=self.num_of_iterations,
            minimum_probability=self.minimum_probability)

        index = gensim.similarities.MatrixSimilarity(corpus_tf_idf)
        print('Finished training LDA model...')

        return lda, index, ids
