import time
import pickle
import warnings
from sklearn.neighbors import NearestNeighbors
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import LdaModel
from utils.pandas_helper import PandasHelper


class LDARecommender:
    def __init__(self):
        self.lda = LdaModel.load('./models/LDA/model')
        self.similarities = LDARecommender.load_pickle_file('./models/LDA/similarities')
        self.num_of_recommendation = 10

    @staticmethod
    def load_pickle_file(file_name):
        file = open(f'{file_name}.pickle', 'rb')
        object_file = pickle.load(file)
        return object_file

    def recommend(self, movie_id):
        start = time.time()

        sims = list(filter(lambda similarity: similarity['id'] == movie_id, self.similarities))

        end = time.time()
        print(f'Recommended in: {end - start} s')

        if len(sims) == 0:
            return None

        return sims[0]['similarities'][:self.num_of_recommendation]
