from models.lda_model import LDAModel


def train_models():
    print('Starting pre-training models...')
    lda_model = LDAModel()
    lda, corpus_tf_idf, df_docs_topics = lda_model.train_model()  # train a LDA model
    lda_model.save_model(lda, corpus_tf_idf, df_docs_topics)  # save model for recommendations use
    print('Finished pre-training models...')
