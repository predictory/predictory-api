class HybridRecommender():
    @staticmethod
    def get_recommendations(user_id, movie_id):
        recommendations = {
            'userId': user_id,
            'movieId': movie_id,
            'recommendations': [
                {'id': 1, 'score': 0.987}
            ]
        }
        return recommendations
