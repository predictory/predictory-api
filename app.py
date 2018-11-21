from flask import Flask
from flask_restful import Api

from db import db
from resources.movie import Movie
from resources.movie_recommendation import MovieRecommendation
from resources.user_recommendation import UserRecommendation
from resources.hybrid_recommendation import HybridRecommendation
from resources.collector import Collector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/recommender'
app.config['SQLALCHEMY_ECHO'] = False
api = Api(app)

api.add_resource(Movie, '/movies')
api.add_resource(MovieRecommendation, '/movies/<int:id>/recommendations')
api.add_resource(UserRecommendation, '/users/<int:id>/recommendations')
api.add_resource(HybridRecommendation, '/recommendations/<int:user_id>/<int:movie_id>')
api.add_resource(Collector, '/collector/<int:id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=3002, debug=True)
