import time
import pickle
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import LdaModel
from utils.pandas_helper import PandasHelper


class LDARecommender:
    def __init__(self):
        self.lda = LdaModel.load('./models/LDA/model')
        self.corpus = LDARecommender.load_pickle_file('./models/LDA/corpus')
        self.df = LDARecommender.load_pickle_file('./models/LDA/df')
        self.num_of_recommendation = 10

    @staticmethod
    def load_pickle_file(file_name):
        file = open(f'{file_name}.pickle', 'rb')
        object_file = pickle.load(file)
        return object_file

    def recommend(self, movie_id):
        start = time.time()

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(self.df)

        movie_topics = self.get_movie_row(movie_id)

        if movie_topics is None:
            return None

        distances, indices = model_knn.kneighbors(movie_topics, n_neighbors=self.num_of_recommendation + 1)
        similarities = 1 - distances.flatten()
        similarities = similarities[1:]
        indices = indices.flatten()
        indices = indices[1:]

        end = time.time()
        print(f'Recommended in: {end - start} s')
        return [{
            'id': PandasHelper.get_id_from_series(self.df.iloc[[indices[index]]]),
            'similarity': float(line)
        } for index, line in enumerate(similarities)]

    def get_movie_row(self, movie_id):
        movie_row = self.df[self.df.index == movie_id]

        if movie_row.empty:
            return None

        row_values = movie_row.values.reshape(1, -1)

        return row_values
