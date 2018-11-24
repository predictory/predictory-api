from envparse import env
from app import FlaskApp
from flask_restful import Api

from db import db
from resources.movie import Movie
from resources.movie_recommendation import MovieRecommendation
from resources.user_recommendation import UserRecommendation
from resources.hybrid_recommendation import HybridRecommendation
from resources.collector import Collector

app = FlaskApp(__name__)

db_user = env('DB_USER', default='root')
db_password = env('DB_PASSWORD', default='')
db_name = env('DB_NAME', default='recommender')
db_host = env('DB_HOST', default='localhost')
db_port = env('DB_PORT', default=3306)
db_dialect = env('DB_DIALECT', default='mysql')

db_user_rec = env('DB_USER_REC', default='root')
db_password_rec = env('DB_PASSWORD_REC', default='')
db_name_rec = env('DB_NAME_REC', default='recommender_rec')
db_host_rec = env('DB_HOST_REC', default='localhost')
db_port_rec = env('DB_PORT_REC', default=3306)
db_dialect_rec = env('DB_DIALECT_REC', default='mysql')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_dialect}+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_BINDS'] = {
    'app': f'{db_dialect}+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',
    'recommender': f'{db_dialect_rec}+pymysql://{db_user_rec}:{db_password_rec}@{db_host_rec}:{db_port_rec}/{db_name_rec}'
}
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
