from flask_restful import Resource
from models.svd_model import SVDModel


class UserRetrain(Resource):

    def put(self):
        print('Started pre-training user-based models...')

        svd_model = SVDModel()
        data, movies, users = svd_model.load_data()
        U, sigma, Vt, predicted_ratings = svd_model.train(data, 90)
        svd_model.save(U, sigma, Vt, predicted_ratings, movies, users)

        print('Finished pre-training user-based models...')

        return {'message': 'Model re-trained.'}, 200
