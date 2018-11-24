from flask import Flask
from db import db


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

    @staticmethod
    def prepare_data():
        db.create_all(bind='recommender')
        # There will be data preparation
