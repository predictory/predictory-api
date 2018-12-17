import os
from flask_restful import fields, marshal
import nltk
import numpy as np
import pandas as pd
from nltk.stem.porter import *
import pickle
from nltk.stem import WordNetLemmatizer
from models.movie import MovieModel
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import models


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
        # Min length of document
        self.min_length = 100
        # Num_topics in LDA
        self.num_topics = 30
        # Filter out tokens that appear in less than `no_below` documents (absolute number)
        self.no_below = 50
        # Filter out tokens that appear in more than `no_above` documents
        self.no_above = 0.2
        # Number of iterations in training LDA model
        self.num_of_iterations = 10000

    @staticmethod
    def lemmatize_stemming(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    @staticmethod
    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(LDAModel.lemmatize_stemming(token))
        return result

    @staticmethod
    def save_pickle_file(file_name, data):
        file_name = f'./models/LDA/{file_name}.pickle'
        mapping_file = open(file_name, 'wb')
        pickle.dump(data, mapping_file)
        mapping_file.close()

    @staticmethod
    def save_model(lda, corpus, docs_topics):
        if not os.path.exists('./models/LDA'):
            os.makedirs('./models/LDA')
        # Save model output
        lda.save('./models/LDA/model')
        # Save corpus
        LDAModel.save_pickle_file('corpus', corpus)
        LDAModel.save_pickle_file('docs_topics', docs_topics)

    def train_model(self):
        movies = MovieModel.query.all()
        data = pd.DataFrame(marshal(movies, movies_fields))

        documents = data['plot']
        ids = data['id']
        processed_docs = documents.map(LDAModel.preprocess)

        print('Start training LDA model...')
        dictionary = gensim.corpora.Dictionary(processed_docs)
        dictionary.filter_extremes(no_below=self.no_below, no_above=self.no_above, keep_n=self.num_of_iterations)
        corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

        tf_idf = models.TfidfModel(corpus)
        corpus_tf_idf = tf_idf[corpus]
        lda = gensim.models.ldamodel.LdaModel(corpus_tf_idf, num_topics=self.num_topics, id2word=dictionary, passes=2,
                                              minimum_probability=0.0)
        docs_topics = np.array([[tup[1] for tup in lst] for lst in lda[corpus_tf_idf]])
        df_docs_topics = pd.DataFrame(docs_topics, index=ids)

        print('Finished training LDA model...')

        return lda, corpus_tf_idf, df_docs_topics
