from flask_restful import Resource
from tasks import retrain


class UserRetrain(Resource):

    @staticmethod
    def put(user_id):
        task = retrain(user_id)
        return {'message': f'Request for retraining for user {user_id} logged as task {task.id}'}, 200
