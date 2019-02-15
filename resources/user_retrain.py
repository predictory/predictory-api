from flask_restful import Resource
import pandas as pd
from models.svd_model import SVDModel


class UserRetrain(Resource):

    @staticmethod
    def put(user_id):
        print('Started pre-training SVD...')

        svd_model = SVDModel()
        data, movies, users = svd_model.load_data()
        U, sigma, Vt, predicted_ratings = svd_model.train(data, 20)
        ratings_df = pd.DataFrame(predicted_ratings, columns=movies, index=users)
        user_row = ratings_df.loc[user_id].to_dict()
        svd_model.save(U, sigma, Vt)
        SVDModel.save_rating(user_id, user_row)

        print('Finished pre-training SVD...')

        return {'message': 'Model re-trained.'}, 200
