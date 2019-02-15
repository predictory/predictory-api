from envparse import env
from flask import Flask
from flask_restful import Api

from db import db
from mongo import mongo
from resources.movie import Movie
from resources.movie_recommendation import MovieRecommendation
from resources.user_recommendation import UserRecommendation
from resources.hybrid_recommendation import HybridRecommendation
from resources.user_retrain import UserRetrain
from resources.movie_topics import MovieTopics

from cli.train import train_models

app = Flask(__name__)


db_user = env('DB_USER', default='root')
db_password = env('DB_PASSWORD', default='')
db_name = env('DB_NAME', default='recommender')
db_host = env('DB_HOST', default='localhost')
db_port = env('DB_PORT', default=3306)
db_dialect = env('DB_DIALECT', default='mysql')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_dialect}+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_ECHO'] = False
app.config["MONGO_URI"] = "mongodb://localhost:27017/recommender"
api = Api(app)
db.init_app(app)
mongo.init_app(app)

api.add_resource(Movie, '/movies')
api.add_resource(MovieRecommendation, '/movies/<int:movie_id>/recommendations')
api.add_resource(UserRecommendation, '/users/<int:user_id>/recommendations')
api.add_resource(HybridRecommendation, '/recommendations/<int:user_id>/<int:movie_id>')
api.add_resource(UserRetrain, '/users/re-train/<int:user_id>')
api.add_resource(MovieTopics, '/movies/<int:movie_id>/topics')


@app.cli.command()
def train():
    train_models()


if __name__ == '__main__':
    app.run(port=3002, debug=True)
