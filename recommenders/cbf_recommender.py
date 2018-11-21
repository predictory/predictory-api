class CBFRecommender():
    @staticmethod
    def get_recommendations(user_id):
        recommendations = {
            'userId': user_id,
            'recommendations': [
                {'id': 1, 'score': 0.987}
            ]
        }
        return recommendations
