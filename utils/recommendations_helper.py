import time
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
from mongo import mongo
from db import db
from sqlalchemy import func, case
from models.movie import MovieModel
from models.genre import GenreModel
from models.user_rating import UserRatingModel
from utils.database_helper import DatabaseHelper


class RecommendationsHelper:

    @staticmethod
    def get_dict(ratings, take=10, skip=0):
        return dict(ratings[skip:skip + take])

    @staticmethod
    def get_similarity_values(user_id, ratings, genres=None, sim_source='tf-idf'):
        start = time.time()

        if sim_source == 'lda':
            mongo_similarities = mongo.db.similarities
        else:
            mongo_similarities = mongo.db.tfidf_similarities

        rated_movies = RecommendationsHelper.get_user_rated_movies(user_id)
        rated_movies = [item['movieId'] for item in rated_movies]

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

        keys = [int(key) for key, value in ratings.items()]
        similarities = mongo_similarities.find({'id': {'$in': keys}})
        similarities = [(
            similarity['id'], [item['similarity'] for item in similarity['similarities'] if item['id'] in rated_movies]
        ) for similarity in similarities]
        movies_similarities = {
            str(similarity[0]): max(similarity[1]) if len(similarity[1]) > 0 else 0 for similarity in similarities
        }

        end = time.time()
        print(f'Similarity computed in: {end - start}s')

        return movies_similarities

    @staticmethod
    def get_pairs(ratings, similarities, stats):
        return [{
            'id': key,
            'rating': float(value),
            'similarity': similarities[key],
            'average_rating': stats[int(key)]['average_rating'],
            'ratings_count': stats[int(key)]['count'],
            'penalized': stats[int(key)]['penalized'],
        } for key, value in ratings.items()]

    @staticmethod
    def get_user_row(user_id):
        mongo_ratings = mongo.db.users_ratings

        user_row = mongo_ratings.find_one({'id': user_id})
        if user_row is not None:
            return user_row['ratings']
        else:
            return None

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
    def get_recommendations(ratings, take, skip, user_id, genres, sim_source='tf-idf'):
        recommended_movies = RecommendationsHelper.get_dict(ratings, take, skip)
        similarities = RecommendationsHelper.get_similarity_values(user_id, recommended_movies, genres, sim_source)
        stats = RecommendationsHelper.get_stats(recommended_movies.keys())

        return RecommendationsHelper.get_pairs(recommended_movies, similarities, stats)

    @staticmethod
    def get_stats(items):
        movies = db.session.query(
                MovieModel.id,
                func.count(UserRatingModel.id),
                func.avg(UserRatingModel.rating),
                func.sum(case([(UserRatingModel.rating == 0, 1)], else_=0))
            ) \
            .join(UserRatingModel, isouter=True)\
            .filter(MovieModel.id.in_(items)) \
            .group_by(MovieModel.id) \
            .all()

        if len(movies) > 0:
            movies = {movie[0]: {
                'count': movie[1],
                'average_rating': movie[2] if movie[2] is not None else 0,
                'penalized': int(movie[3])
            } for movie in movies}

        return movies

    @staticmethod
    def get_user_movies_custom_based(rated_movies, user_id, include_rated=False, rec_type='item-based',
                                     sim_type='cosine'):
        data, movies, users = DatabaseHelper.load_data_matrix()
        data_matrix = pd.DataFrame(data.todense(), columns=movies, index=users)

        if rec_type == 'item-based':
            similarity = 1 - pairwise_distances(data_matrix.transpose().values, metric=sim_type)
            prediction = data_matrix.values.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
        else:
            similarity = 1 - pairwise_distances(data_matrix.values, metric=sim_type)
            mean_user_rating = data_matrix.values.mean(axis=1)
            ratings_diff = (data_matrix.values - mean_user_rating[:, np.newaxis])
            prediction = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array(
                [np.abs(similarity).sum(axis=1)]).T

        prediction = pd.DataFrame(prediction, columns=movies, index=users)
        user_row = prediction.loc[user_id].to_dict()

        if not include_rated:
            for movie in rated_movies:
                try:
                    del user_row[movie['movieId']]
                except:
                    print('Movie not found')
        else:
            penalized_movies = list(filter(lambda movie: movie['rating'] == 0, rated_movies))
            for movie in penalized_movies:
                try:
                    del user_row[movie['movieId']]
                except:
                    print('Movie not found')

        return user_row

    @staticmethod
    def sort(recommendations, keys):
        data = sorted(recommendations, key=lambda x: [x[key] for key in keys if key in x],
                      reverse=True)
        return data

    @staticmethod
    def filter_not_fav_genres(ratings, not_fav_genres):
        genres_ids = not_fav_genres.split(',')
        genres_items = DatabaseHelper.get_movies_for_genres(genres_ids)

        if len(genres_items) > 0:
            ratings = [item for item in ratings if int(item[0]) not in genres_items]

        return ratings

    @staticmethod
    def favor_fav_genres(ratings, not_fav_genres):
        genres_ids = not_fav_genres.split(',')
        genres_items = DatabaseHelper.get_movies_for_genres(genres_ids)

        if len(genres_items) > 0:
            ratings = [(item[0], item[1] * 1.5 if int(item[0]) in genres_items else item[1]) for item in ratings]

        return ratings

    @staticmethod
    def process_genres(ratings, fav_genres, not_fav_genres):
        if not_fav_genres is not None:
            ratings = RecommendationsHelper.filter_not_fav_genres(ratings, not_fav_genres)
        if fav_genres is not None:
            ratings = RecommendationsHelper.favor_fav_genres(ratings, fav_genres)
        num_of_ratings = len(ratings)

        return ratings, num_of_ratings

    @staticmethod
    def compute_augmented_rating(recommendations):
        for row in recommendations:
            row['augmented_rating'] = row['rating'] * (1 + row['es_score']) if row['rating'] > 0 else row['es_score']
        return recommendations
