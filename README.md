# Predictory - API

> Recommender API for [Predictory APP](https://github.com/predictory/predictory-app)

## Installation

First of all, install [virtual environment](https://virtualenv.pypa.io/) on your machine.
Then, create virtual environment (more details in [this guide](https://docs.python-guide.org/dev/virtualenvs/)).

``` bash
virtualenv venv
```

Then, activate virtual environment

``` bash
source venv/bin/activate
```

### Getting required packages

``` bash
pip install -r requirements.txt
```

### Configuration

For project configuration, you can use environment variables on your machine, or you can change configuration of project directly in `app_config.py`.

```
db_user = env('DB_USER', default='root')
db_password = env('DB_PASSWORD', default='')
db_name = env('DB_NAME', default='recommender')
db_host = env('DB_HOST', default='localhost')
db_port = env('DB_PORT', default=3306)
db_dialect = env('DB_DIALECT', default='mysql')
```

Also, you need to install and configure MongoDB and Redis. Configuration is in `app_config.py` too.

```
app_config = {
    'mongo_uri': 'mongodb://localhost:27017/recommender',
    'redis_uri': env('REDIS_URL', default='redis://localhost:6379')
}
```

### Database setup, data preparation, database population

All of these steps are performed by [Predictory APP](https://github.com/predictory/predictory-app).
Follow instructions in APP repo to prepare data for this API.

### Training recommender API

To train recommender API, run command:

```
flask train
```

It will take some time.

You can also start training by accessing route `/train`.

## Running recommender API

To start the API, run command

```
python main.py
```

It's not recommended to use this command in production mode. For that, use package `uwsgi` and configure your server properly (you can find more information [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)).

## Running tasks queue

The project is using redis queue for retraining tasks (created with [huey](https://github.com/coleifer/huey)).  For proper functioning of the application, you need to run huey worker (for processing incoming tasks) as well. To start huey worker, run
```
python venv/Scripts/huey_consumer.py run_huey.huey
```
(this command works for Windows, for Linux replace Scripts folder in the path with `bin` folder)
