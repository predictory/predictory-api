from flask import Flask
from huey import RedisHuey
from db import db
from mongo import mongo
from app_config import app_config


def create_huey_app():
    app = Flask('huey-app')
    app.config['SQLALCHEMY_DATABASE_URI'] = app_config['db_uri']
    app.config['SQLALCHEMY_ECHO'] = app_config['alchemy_echo']
    app.config['MONGO_URI'] = app_config['mongo_uri']
    db.init_app(app)
    mongo.init_app(app)

    return app


huey = RedisHuey(url=app_config['redis_uri'])
