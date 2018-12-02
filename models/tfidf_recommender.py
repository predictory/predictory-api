import time
import pickle


class TFIDFRecommender:
    def __init__(self):
        self.indices = TFIDFRecommender.load_pickle_file('./models/TFIDF/indices')
        self.similarities = TFIDFRecommender.load_pickle_file('./models/TFIDF/similarities')

    @staticmethod
    def load_pickle_file(file_name):
        file = open(f'{file_name}.pickle', 'rb')
        object_file = pickle.load(file)
        return object_file

    def recommend(self, movie_id, n=10):
        start = time.time()

        idx = self.indices[movie_id]
        sim_scores = list(enumerate(self.similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:int(n) + 1]
        movie_indices = [{'id': int(self.indices[self.indices == i[0]].index.tolist()[0]), 'similarity': i[1]} for i in sim_scores]

        end = time.time()
        print(f'Finished in: {end - start}')

        return movie_indices
