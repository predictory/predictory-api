import pandas as pd
from models.lda_model import LDAModel
from models.svd_model import SVDModel
from models.tfidf_model import TFIDFModel


def train_svd():
    svd_model = SVDModel()
    data, movies, users = svd_model.load_data()
    U, sigma, Vt, predicted_ratings = svd_model.train(data, 20)
    ratings_df = pd.DataFrame(predicted_ratings, columns=movies, index=users)

    print('Saving SVD model')
    svd_model.save(U, sigma, Vt)
    SVDModel.save_ratings(ratings_df)


def train_tf_idf():
    tfidf_model = TFIDFModel()
    indices, similarities = tfidf_model.train()

    print('Saving TF-IDF model')
    tfidf_model.save_similarities(similarities, indices)

    print('Saving TF-IDF similarities distribution')
    tfidf_model.save_distributions(similarities)


def train_lda():
    lda_model = LDAModel()
    lda, corpus, index, ids = lda_model.train_model()
    topics = lda_model.get_topics(lda, corpus, ids)
    similarities = lda_model.get_similarities(index, ids)

    lda_model.save_model(lda)
    lda_model.save_topics(topics)
    lda_model.save_similarities(similarities)


def train_models():
    print('Started training models')
    train_svd()
    train_tf_idf()
    train_lda()
    print('Finished training models')
