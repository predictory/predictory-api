# Hybrid recommender API

> Recommender API for [Hybrid recommender APP](https://github.com/Fir3st/hybrid-recommender-app)

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

For project configuration, you can use environment variables on your machine, or you can change configuration of project directly in `app.py`.

``` bash
db_user = env('DB_USER', default='root')
db_password = env('DB_PASSWORD', default='')
db_name = env('DB_NAME', default='recommender')
db_host = env('DB_HOST', default='localhost')
db_port = env('DB_PORT', default=3306)
db_dialect = env('DB_DIALECT', default='mysql')
```

Also, you need to install and configure MongoDB. Configuration for MongoDB is in `app.py` too.

``` bash
app.config["MONGO_URI"] = "mongodb://localhost:27017/recommender"
```

### Database setup, data preparation, database population

All of these steps are performed by [Recommender APP](https://github.com/Fir3st/hybrid-recommender-app).
Follow instructions in APP repo to prepare data for this API.

### Training recommender API

To train recommender API, run command:

``` bash
flask train
```

It will take some time.

You can also start training by accessing route `/train`.

## Running recommender API

To start the API, run command

``` bash
python app.py
```

It's not recommended to use this command in production mode. For that, use package `uwsgi` and configure your server properly (you can find more information [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)).
