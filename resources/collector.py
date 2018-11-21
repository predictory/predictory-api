from flask_restful import Resource, reqparse

class Collector(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('test',
                        required=True,
                        help="Just for testing"
                        )

    def post(self, id):
        data = Collector.parser.parse_args()
        response = {
            'id': id
        }
        return response, 200
