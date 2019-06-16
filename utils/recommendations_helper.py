from mongo import mongo
from db import db
from sqlalchemy import func, case
from models.movie import MovieModel
from models.genre import GenreModel
from models.user_rating import UserRatingModel


class RecommendationsHelper:

    @staticmethod
    def get_dict(ratings, take=10, skip=0):
        return dict(ratings[skip:skip + take])

    @staticmethod
    def get_similarity_values(user_id, ratings, genres=None):
        mongo_similarities = mongo.db.tfidf_similarities
        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)
        rated_movies = [item['movieId'] for item in rated_movies]
        movies_similarities = dict()

        if genres is not None:
            genres_ids = genres.split(',')
            movies = db.session.query(MovieModel.id) \
                .join(MovieModel.genres)\
                .filter(MovieModel.id.in_(rated_movies)) \
                .filter(GenreModel.id.in_(genres_ids)) \
                .group_by(MovieModel.id) \
                .having(func.count(GenreModel.id) == len(genres_ids))\
                .all()

            rated_movies = [movie[0] for movie in movies]

        for key, value in ratings.items():
            similarities = mongo_similarities.find_one({'id': int(key)})
            similarities = similarities['similarities']
            similar_items = [item for item in similarities if item['id'] in rated_movies]
            similarity = None
            if len(similar_items) > 0:
                similarity = 0
                for item in similar_items:
                    if item['similarity'] > similarity:
                        similarity = item['similarity']

            movies_similarities[key] = similarity

        return movies_similarities

    @staticmethod
    def get_pairs(ratings, similarities, stats):
        return [{
            'id': key,
            'rating': float(value),
            'similarity': similarities[key],
            'average_rating': stats[key]['average_rating'],
            'ratings_count': stats[key]['count'],
            'penalized': stats[key]['penalized'],
        } for key, value in ratings.items()]

    @staticmethod
    def get_user_row(user_id):
        mongo_ratings = mongo.db.users_ratings

        user_row = mongo_ratings.find_one({'id': user_id})
        return user_row['ratings']

    @staticmethod
    def get_user_rated_movies(user_id):
        rated_movies = db.session.query(UserRatingModel).filter_by(userId=user_id).all()
        return [row.__dict__ for row in rated_movies]

    @staticmethod
    def get_user_movies(rated_movies, user_id, include_rated=False):
        user_row = RecommendationsHelper.get_user_row(user_id)

        if not include_rated:
            for movie in rated_movies:
                try:
                    del user_row[str(movie['movieId'])]
                except:
                    print('Movie not found')
        else:
            penalized_movies = list(filter(lambda movie: movie['rating'] == 0, rated_movies))
            for movie in penalized_movies:
                try:
                    del user_row[str(movie['movieId'])]
                except:
                    print('Movie not found')

        return user_row

    @staticmethod
    def get_recommendations(ratings, take, skip, user_id, genres):
        recommended_movies = RecommendationsHelper.get_dict(ratings, take, skip)
        similarities = RecommendationsHelper.get_similarity_values(user_id, recommended_movies, genres)
        stats = RecommendationsHelper.get_stats(recommended_movies)

        return RecommendationsHelper.get_pairs(recommended_movies, similarities, stats)

    @staticmethod
    def get_stats(items):
        keys = items.keys()
        movies = db.session.query(
                MovieModel.id,
                func.count(UserRatingModel.id),
                func.avg(UserRatingModel.rating),
                func.sum(case([(UserRatingModel.rating == 0, 1)], else_=0))
            ) \
            .join(UserRatingModel)\
            .filter(MovieModel.id.in_(keys)) \
            .group_by(MovieModel.id) \
            .all()

        if len(movies) > 0:
            movies = {movie[0]: {
                'count': movie[1],
                'average_rating': movie[2],
                'penalized': int(movie[3])
            } for movie in movies}

        return movies
