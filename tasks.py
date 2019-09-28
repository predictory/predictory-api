import pandas as pd
from huey_queue import create_huey_app
from huey_queue import huey
from models.svd_model import SVDModel
from utils.database_helper import DatabaseHelper


@huey.task()
def retrain(user_id):
    app = create_huey_app()
    with app.app_context():
        svd_model = SVDModel()
        data, movies, users = DatabaseHelper.load_data_matrix()
        U, sigma, Vt, predicted_ratings = svd_model.train(data, 20)
        ratings_df = pd.DataFrame(predicted_ratings, columns=movies, index=users)

        if user_id in ratings_df.index:
            user_row = ratings_df.loc[user_id].to_dict()
            svd_model.save(U, sigma, Vt)
            SVDModel.save_rating(user_id, user_row)
        else:
            print(f'[Retrain]: User with id {user_id} has no recommendations')
