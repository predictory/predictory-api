from flask_restful import Resource
from cli.train import train_models


class Retrain(Resource):

    @staticmethod
    def put():
        train_models()

        return {'message': 'Recommender trained.'}, 200
