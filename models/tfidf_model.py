import os
from flask_restful import fields, marshal
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.movie import MovieModel

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
fields = {
    'id': fields.Integer,
    'title': fields.String,
    'plot': fields.String
}


class TFIDFModel:
    @staticmethod
    def _save_pickle_file(file_name, data):
        file_name = f'./models/TFIDF/{file_name}.pickle'
        mapping_file = open(file_name, 'wb')
        pickle.dump(data, mapping_file)
        mapping_file.close()

    def save(self, indices, similarities):
        if not os.path.exists('./models/TFIDF'):
            os.makedirs('./models/TFIDF')

        self._save_pickle_file('indices', indices)
        self._save_pickle_file('similarities', similarities)

    @staticmethod
    def train():
        print('Start training TF-IDF model...')

        movies = MovieModel.query.all()
        data = pd.DataFrame(marshal(movies, fields))
        tfidf_matrix = tf.fit_transform(data['plot'])
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(data.index, index=data['id'])

        print('Finished training TF-IDF model...')

        return indices, cosine_similarities
