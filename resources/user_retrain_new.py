from flask_restful import Resource
from tasks import retrain_new


class UserRetrainNew(Resource):

    @staticmethod
    def put(user_id):
        task = retrain_new(user_id)
        return {'message': f'Request for retraining for user {user_id} logged as task {task.id}'}, 200
