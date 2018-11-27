import time
import pickle
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import LdaModel


class LDARecommender:
    def __init__(self):
        self.lda = LdaModel.load('./models/LDA/model')
        self.corpus = LDARecommender.load_pickle_file('./models/LDA/corpus')
        self.docs_topics = LDARecommender.load_pickle_file('./models/LDA/docs_topics')
        self.num_of_recommendation = 10

    @staticmethod
    def load_pickle_file(file_name):
        file = open(f'{file_name}.pickle', 'rb')
        object_file = pickle.load(file)
        return object_file

    def recommend(self, movie_id):
        start = time.time()

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(self.docs_topics)

        distances, indices = model_knn.kneighbors(self.docs_topics.iloc[movie_id, :].values.reshape(1, -1),
                                                  n_neighbors=self.num_of_recommendation + 1)
        similarities = 1 - distances.flatten()
        similarities = similarities[1:]
        indices = indices.flatten()
        indices = indices[1:]

        end = time.time()
        print(f'Recommended in: {end - start} s')
        return [{str(indices[index]): float(line)} for index, line in enumerate(similarities)]
