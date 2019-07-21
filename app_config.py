from envparse import env

db_user = env('DB_USER', default='root')
db_password = env('DB_PASSWORD', default='')
db_name = env('DB_NAME', default='recommender')
db_host = env('DB_HOST', default='localhost')
db_port = env('DB_PORT', default=3306)
db_dialect = env('DB_DIALECT', default='mysql')

app_config = {
    'db_uri': f'{db_dialect}+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',
    'mongo_uri': 'mongodb://localhost:27017/recommender',
    'redis_uri': env('REDIS_URL', default='redis://localhost:6379'),
    'alchemy_echo': False
}
