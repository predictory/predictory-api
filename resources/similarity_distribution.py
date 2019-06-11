from flask_restful import Resource
from mongo import mongo
import json


class SimilarityDistribution(Resource):
    @staticmethod
    def get():
        mongo_distributions = mongo.db.similarities_distribution
        distributions = mongo_distributions.find()

        return [{
            'startValue': record['startValue'],
            'endValue': record['endValue'],
            'count': record['count']
        } for record in distributions], 200
