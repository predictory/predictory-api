from flask import Flask
from flask_restful import Api

from db import db
from mongo import mongo
from app_config import app_config
from resources.movie import Movie
from resources.movie_recommendation import MovieRecommendation
from resources.user_recommendation import UserRecommendation
from resources.hybrid_recommendation import HybridRecommendation
from resources.user_retrain import UserRetrain
from resources.retrain import Retrain
from resources.search import Search
from resources.similarity_distribution import SimilarityDistribution
from resources.cbf_playground import CBFPlayground
from resources.cb_playground import CBPlayground

from cli.train import train_models


def create_app():
    app = Flask('app')
    app.config['SQLALCHEMY_DATABASE_URI'] = app_config['db_uri']
    app.config['SQLALCHEMY_ECHO'] = app_config['alchemy_echo']
    app.config['MONGO_URI'] = app_config['mongo_uri']

    api = Api(app)
    db.init_app(app)
    mongo.init_app(app)

    api.add_resource(Movie, '/movies')
    api.add_resource(SimilarityDistribution, '/movies/similarities-distribution')
    api.add_resource(MovieRecommendation, '/movies/<int:movie_id>/recommendations')
    api.add_resource(UserRecommendation, '/users/<int:user_id>/recommendations')
    api.add_resource(HybridRecommendation, '/recommendations/<int:user_id>/<int:movie_id>')
    api.add_resource(UserRetrain, '/train/users/<int:user_id>')
    api.add_resource(Retrain, '/train')
    api.add_resource(Search, '/search/<int:user_id>')
    api.add_resource(CBFPlayground, '/users-playground/<int:user_id>')
    api.add_resource(CBPlayground, '/movies-playground/<int:movie_id>')

    @app.cli.command()
    def train():
        train_models()

    return app
