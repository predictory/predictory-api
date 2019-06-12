from flask_restful import fields, marshal
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.movie import MovieModel
from mongo import mongo
import json
import itertools
import numpy as np

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
fields = {
    'id': fields.Integer,
    'title': fields.String,
    'plot': fields.String
}


class TFIDFModel:
    @staticmethod
    def save_similarities(similarities, indices):
        mongo_similarities = mongo.db.tfidf_similarities
        mongo_similarities.delete_many({})

        for index, row in enumerate(similarities):
            TFIDFModel.save_similarity(indices[index], row, indices)

    @staticmethod
    def save_similarity(movie_id, similarities, indices):
        max_sim = 50
        mongo_similarities = mongo.db.tfidf_similarities
        mongo_similarities.delete_many({'id': int(movie_id)})

        sim_scores = list(enumerate(similarities))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:int(max_sim) + 1]
        movie_indices = [{
            'id': int(indices[i[0]]),
            'similarity': float(i[1])
        } for i in sim_scores]
        movie_indices = json.dumps(movie_indices)

        row = {
            'id': int(movie_id),
            'similarities': json.loads(movie_indices)
        }

        mongo_similarities.insert_one(row)

    @staticmethod
    def train():
        print('Started training TF-IDF model...')

        movies = MovieModel.query.all()
        data = pd.DataFrame(marshal(movies, fields))
        tfidf_matrix = tf.fit_transform(data['plot'])
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        print('Finished training TF-IDF model...')

        return data['id'], cosine_similarities

    @staticmethod
    def save_distributions(similarities):
        mongo_distributions = mongo.db.similarities_distribution
        mongo_distributions.delete_many({})
        merged = list(itertools.chain(*similarities))
        merged = [value for value in merged if value != 0 and value < 1]
        merged.sort()
        counted = np.array(np.unique(merged, return_counts=True)).T
        n = 100
        k, m = divmod(len(counted), n)
        divided_values = list(counted[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
        for row in divided_values:
            TFIDFModel.save_distribution(row[0][0], row[len(row) - 1][0], sum(subrow[1] for subrow in row))

    @staticmethod
    def save_distribution(start_value, end_value, count):
        mongo_distributions = mongo.db.similarities_distribution

        row = {
            'startValue': start_value,
            'endValue': end_value,
            'count': int(count)
        }

        mongo_distributions.insert_one(row)
